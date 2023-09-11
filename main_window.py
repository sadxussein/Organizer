import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QAbstractItemView, QListView, QPushButton, QVBoxLayout, QTableView, \
    QScrollArea, QHBoxLayout, QLabel, QLineEdit, QAction, QMessageBox, QTabWidget, QMenu

from entity_list_view import EntityListView
from job_list_delegate import JobListDelegate
from job_list_model import JobListModel
from task import Task
from task_list_model import TaskListModel
from task_list_delegate import TaskListDelegate


# TODO: create new task form
# TODO: connect them with calendar
# TODO: create graphs for tasks
# TODO: create task groups, maybe even tags
# TODO: try visualize tasks as icons in list view
# TODO: make one-time tasks subsidiary of tasks
# TODO: create options class


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # meta variables
        self._currently_selected_task = None
        self._currently_selected_job = None
        self._is_allowed_multiple_tasks_running = False
        # elements of the window
        self.menu_bar = self.menuBar()
        self.file_menu_bar = self.menu_bar.addMenu("File")
        self.options_menu_bar = self.menu_bar.addMenu("Options")
        self.save_menu_bar_action = QAction("Save", self)
        self.exit_menu_bar_action = QAction("Exit", self)
        self.allow_multiple_tasks_menu_bar_action = QAction("Allow multiple tasks running", self)
        # main widget
        self.central_widget = QWidget(self)
        self.layout = QVBoxLayout()
        # tabs
        self.tab_widget = QTabWidget(self)
        self.task_list_view_widget = QWidget()
        self.task_list_view = EntityListView(self.task_list_view_widget)
        self.task_ordered_view_widget = QWidget()
        self.task_ordered_view = QListView(self.task_ordered_view_widget)
        self.task_graph_view_widget = QWidget()
        self.task_graph_view = QListView(self.task_graph_view_widget)      # TODO: use proper view for drawing graphs
        self.job_list_view_widget = QWidget()
        self.job_list_view = QListView(self.job_list_view_widget)
        # start/end buttons
        self.start_task_button = QPushButton("Start task")
        self.end_task_button = QPushButton("End task")
        # task view area
        self.task_view_scroll_area = QScrollArea()
        self.task_view_scroll_content = QWidget()
        self.task_view_layout = QVBoxLayout(self.task_view_scroll_content)
        self.task_view_element_pairs = []
        self.save_tasks_button = QPushButton("Save tasks")
        # models & loading data from JSON file
        self._tasks = []
        self._jobs = []
        self.open_json_file()
        self._task_list_model = TaskListModel(self._tasks)
        self._task_list_view_selection_model = None
        self._job_list_model = JobListModel(self._jobs)
        self._job_list_view_selection_model = None
        # delegates
        self._task_list_delegate = TaskListDelegate()
        self._job_list_delegate = JobListDelegate()
        # initializing main elements of the window
        self.init_window()

    # setting up window's elements properties
    def init_window(self):
        # menu bar
        self.file_menu_bar.addAction(self.save_menu_bar_action)
        self.file_menu_bar.addSeparator()
        self.file_menu_bar.addAction(self.exit_menu_bar_action)
        self.save_menu_bar_action.triggered.connect(self.save_json_file)
        self.exit_menu_bar_action.triggered.connect(self.close)
        self.options_menu_bar.addAction(self.allow_multiple_tasks_menu_bar_action)
        self.allow_multiple_tasks_menu_bar_action.setCheckable(True)
        self.allow_multiple_tasks_menu_bar_action.setChecked(False)
        self.allow_multiple_tasks_menu_bar_action.triggered.connect(self.on_allow_multiple_tasks_running)
        # widget to which other elements are attached to
        self.setCentralWidget(self.central_widget)
        # all tasks in a list/tab
        # task list view
        # self.task_list_view.setSelectionMode(QAbstractItemView.SingleSelection)   # FIXME: is by default single mode?
        self.task_list_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.task_list_view.customContextMenuRequested.connect(lambda event: self.show_context_menu(event, self.task_list_view))
        # self.task_list_view.setDragEnabled(True)  # FIXME: drag n drops necessary?
        # self.task_list_view.setAcceptDrops(True)
        # self.task_list_view.setDropIndicatorShown(True)
        self.task_list_view.setModel(self._task_list_model)
        self.task_list_view.setItemDelegate(self._task_list_delegate)     # FIXME: commented for testing icon view
        self._task_list_view_selection_model = self.task_list_view.selectionModel()
        self._task_list_view_selection_model.selectionChanged.connect(self.on_selection_changed)
        # TODO: task ordered view
        # TODO: task graph view
        # job list view
        self.job_list_view.setModel(self._job_list_model)
        self.job_list_view.setItemDelegate(self._job_list_delegate)
        self.job_list_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.job_list_view.customContextMenuRequested.connect(lambda event: self.show_context_menu(event, self.job_list_view))
        self._job_list_view_selection_model = self.job_list_view.selectionModel()
        self._job_list_view_selection_model.selectionChanged.connect(self.on_selection_changed)
        # task detailed view
        labels = ["Register time", "Currently running", "Start time", "End time", "Time ranges"]
        for el in labels:
            pair_layout = QHBoxLayout()
            label = QLabel(f"{el}")
            line_edit = QLineEdit()
            pair_layout.addWidget(label)
            pair_layout.addWidget(line_edit)
            self.task_view_layout.addLayout(pair_layout)
            self.task_view_element_pairs.append((label, line_edit))
        self.task_view_scroll_area.setWidget(self.task_view_scroll_content)
        self.task_view_scroll_area.setWidgetResizable(True)
        # buttons, names are self-explanatory
        self.start_task_button.clicked.connect(self.on_start_task)
        self.end_task_button.clicked.connect(self.on_end_task)
        self.save_tasks_button.clicked.connect(self.save_json_file)
        # adding elements to tab layout
        self.tab_widget.addTab(self.task_list_view, "Task list")
        self.tab_widget.addTab(self.task_ordered_view, "Ordered task list")
        self.tab_widget.addTab(self.task_graph_view, "Task graph")
        self.tab_widget.addTab(self.job_list_view, "Job list")
        # adding elements to main layout
        self.layout.addWidget(self.tab_widget)
        self.layout.addWidget(self.start_task_button)
        self.layout.addWidget(self.end_task_button)
        self.layout.addWidget(self.task_view_scroll_area)
        self.layout.addWidget(self.save_tasks_button)
        # applying layout to central widget
        self.central_widget.setLayout(self.layout)
        # window size
        self.setGeometry(200, 200, 600, 600)

    # opening file and extracting data
    def open_json_file(self):
        with open("tasks.json", 'r') as file:   # JSON file containing our tasks
            json_data = json.load(file)         # store all our tasks which now need to be parsed into simple list
        # import from file into model
        print("json", json_data)    # FIXME: remove debug
        self.json_to_models(json_data)

    # transforming JSON data to multiple models for views
    def json_to_models(self, data):
        for el in data:
            self._tasks.append(Task(el["name"], el["registerTime"], el["isRunning"],
                                    el["startTime"], el["endTime"], el["timeRanges"]))

    # TODO: saving to file results of program's work
    def save_json_file(self):
        json_data = self.model_to_json()
        with open("tasks.json", "w") as file:
            json.dump(json_data, file, indent=4)

    # TODO: transforming model back to JSON to save in file
    def model_to_json(self):
        json_result_data = []
        for task in self._tasks:
            json_result_data.append(task.prepare_task_for_json_export())
        return json_result_data

    # add task button function
    def on_add_task(self):
        rows = self._task_list_model.rowCount()
        self._task_list_model.insertRows(rows, 1)

    # delete task button function
    def on_delete_task(self):
        # TODO: rewrite for usage of _task_list_selection_model
        selection_model = self.task_list_view.selectionModel()
        selected_indexes = selection_model.selectedIndexes()
        # in case if in the future task list view will support multi-selection
        for index in selected_indexes:
            self._task_list_model.removeRows(index.row(), 1)
            # print(self._tasks) FIXME: remove debug

    def on_rename_task(self):
        selection_model = self.task_list_view.selectionModel()
        selected_indexes = selection_model.selectedIndexes()
        for index in selected_indexes:
            self.task_list_view.edit(index)

    def on_edit_task(self):
        pass

    def on_start_task(self):
        # print(self._currently_selected_task)    # FIXME: remove debug
        if not self._is_allowed_multiple_tasks_running:
            if self._currently_selected_task is not None and not any([task.is_task_running() for task in self._tasks]):
                self._tasks[self._currently_selected_task].start_task()
                self.update_task_view()
            else:
                self.show_error_message()
        else:
            if self._currently_selected_task is not None:
                self._tasks[self._currently_selected_task].start_task()
                self.update_task_view()

    def on_end_task(self):      # FIXME: only allow when task isRunning == True
        # print(self._currently_selected_task)    # FIXME: remove debug
        if self._currently_selected_task is not None:
            self._tasks[self._currently_selected_task].end_task()
            self.update_task_view()

    @staticmethod
    def __on_add_entity(view):
        rows = view.model().rowCount()
        view.model().insertRows(rows, 1)

    @staticmethod
    def __on_delete_entity(view):
        for index in view.selectionModel().selectedIndexes():
            view.model().removeRows(index.row(), 1)

    @staticmethod
    def __on_rename_entity(view):
        for index in view.selectionModel().selectedIndexes():
            view.edit(index)

    # TODO: implement edit window
    @staticmethod
    def __on_edit_job(view):
        pass

    # updating index of selected task
    def on_selection_changed(self):
        selection_model = self.task_list_view.selectionModel()
        selected_indexes = selection_model.selectedIndexes()
        for index in selected_indexes:
            # TODO: passing index, while having protected variable of selected task
            self._currently_selected_task = index.row()
            self.update_task_view()

    def on_selection_changed_jobs(self):    # TODO: create unified function for views selection
        selection_model = self.job_list_view.selectionModel()
        selected_indexes = selection_model.selectedIndexes()
        for index in selected_indexes:
            self._currently_selected_job = index.row()
            self.update_task_view()

    def update_task_view(self):
        current_task = self._tasks[self._currently_selected_task].get_task("USER")
        for i in range(len(current_task)):
            self.task_view_element_pairs[i][1].setText(f"{current_task[i]}")

    # TODO: need to think about this logic, it might be necessary to save application status of options to prevent
    #   multiple tasks running when it is not allowed after loading
    def on_allow_multiple_tasks_running(self):
        if self._is_allowed_multiple_tasks_running:
            self._is_allowed_multiple_tasks_running = False
        else:
            self._is_allowed_multiple_tasks_running = True

    def show_error_message(self):
        error_dialog_box = QMessageBox(self)
        error_dialog_box.setIcon(QMessageBox.Critical)
        error_dialog_box.setWindowTitle("Error")
        error_dialog_box.setText("Not allowed running multiple.")
        error_dialog_box.setInformativeText("Check program options.")
        error_dialog_box.setStandardButtons(QMessageBox.Ok)
        error_dialog_box.exec_()

    def show_context_menu(self, event, view):
        context_menu = QMenu()
        add_action = QAction("Add job", self)
        delete_action = QAction("Delete job", self)
        rename_action = QAction("Rename job", self)
        edit_action = QAction("Edit job", self)

        add_action.triggered.connect(lambda: self.__on_add_entity(view))
        delete_action.triggered.connect(lambda: self.__on_delete_entity(view))
        rename_action.triggered.connect(lambda: self.__on_rename_entity(view))
        edit_action.triggered.connect(lambda: self.__on_edit_job(view))

        if any(view.selectionModel().selectedIndexes()):
            context_menu.addAction(add_action)
            context_menu.addAction(delete_action)
            context_menu.addAction(rename_action)
            context_menu.addAction(edit_action)
        else:
            context_menu.addAction(add_action)

        context_menu.exec_(view.mapToGlobal(event))

    def on_view_clicked(self, event, view):
        index = view.indexAt(event.pos())
        if not index.isValid():
            view.clearSelection()
        super(MainWindow, self).mousePressEvent(event)
