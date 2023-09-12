import json

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QListView, QPushButton, QVBoxLayout, \
    QScrollArea, QHBoxLayout, QLabel, QLineEdit, QAction, QMessageBox, QTabWidget, QMenu

import constants
from constants import isTaskRunningRole
from entity_list_view import EntityListView
from job import Job
from job_list_delegate import JobListDelegate
from job_list_model import JobListModel
from task import Task
from task_list_model import TaskListModel
from task_list_delegate import TaskListDelegate


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
        self._currently_selected_entity_index = None
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
        self.task_ordered_view = EntityListView(self.task_ordered_view_widget)
        self.task_graph_view_widget = QWidget()
        self.task_graph_view = QListView(self.task_graph_view_widget)      # TODO: use proper view for drawing graphs
        self.job_list_view_widget = QWidget()
        self.job_list_view = EntityListView(self.job_list_view_widget)
        # task view area
        self.task_view_scroll_area = QScrollArea()
        self.task_view_scroll_content = QWidget()
        self.task_view_layout = QVBoxLayout(self.task_view_scroll_content)
        self.task_view_element_pairs = []
        self.save_tasks_button = QPushButton("Save tasks")
        # models & loading data from JSON file
        self._tasks = []
        self._jobs = []
        self._task_list_model = TaskListModel(self._tasks)
        self._task_list_view_selection_model = None
        self._job_list_model = JobListModel(self._jobs)
        self._job_list_view_selection_model = None
        # delegates
        self._task_list_delegate = TaskListDelegate()
        self._job_list_delegate = JobListDelegate()
        # initializing main elements of the window
        self.__init_window()
        # file handling
        self.__open_tasks_json_file()
        self.__open_jobs_json_file()

    # setting up window's elements properties
    def __init_window(self):
        # menu bar
        self.file_menu_bar.addAction(self.save_menu_bar_action)
        self.file_menu_bar.addSeparator()
        self.file_menu_bar.addAction(self.exit_menu_bar_action)
        self.save_menu_bar_action.triggered.connect(self.__save_to_files)
        self.exit_menu_bar_action.triggered.connect(self.close)
        self.options_menu_bar.addAction(self.allow_multiple_tasks_menu_bar_action)
        self.allow_multiple_tasks_menu_bar_action.setCheckable(True)
        self.allow_multiple_tasks_menu_bar_action.setChecked(False)
        self.allow_multiple_tasks_menu_bar_action.triggered.connect(self.on_allow_multiple_tasks_running)
        # widget to which other elements are attached to
        self.setCentralWidget(self.central_widget)
        # all tasks in a list/tab
        # task list view
        self.task_list_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.task_list_view.customContextMenuRequested.connect(lambda event: self.show_context_menu(event, self.task_list_view))
        self.task_list_view.setModel(self._task_list_model)
        self.task_list_view.setItemDelegate(self._task_list_delegate)
        self.task_list_view.setEditTriggers(QListView.NoEditTriggers)   # disable default element editing by double click
        # self.task_list_view.doubleClicked.connect(lambda index: self.on_start_task(index))
        self.task_list_view.doubleClicked.connect(lambda index: self.__on_task_switch(index))
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
        self.save_tasks_button.clicked.connect(self.__save_to_files)
        # adding elements to tab layout
        self.tab_widget.addTab(self.task_list_view, "Task list")
        self.tab_widget.addTab(self.task_ordered_view, "Ordered task list")
        self.tab_widget.addTab(self.task_graph_view, "Task graph")
        self.tab_widget.addTab(self.job_list_view, "Job list")
        # adding elements to main layout
        self.layout.addWidget(self.tab_widget)
        self.layout.addWidget(self.task_view_scroll_area)
        self.layout.addWidget(self.save_tasks_button)
        # applying layout to central widget
        self.central_widget.setLayout(self.layout)
        # window size
        self.setGeometry(200, 200, 600, 600)

    # opening file and extracting data
    def __open_tasks_json_file(self):
        with open("tasks.json", 'r') as file:   # JSON file containing our tasks
            json_data = json.load(file)         # store all our tasks which now need to be parsed into simple list
        # import from file into model
        self.task_list_view.model().prepare_json_for_model(json_data)

    # transforming JSON data to multiple models for views
    # def json_to_model(self, data):
    #     for el in data:
    #         self._tasks.append(Task(el["name"], el["registerTime"], el["isRunning"],
    #                                 el["startTime"], el["endTime"], el["timeRanges"]))

    # TODO: saving to file results of program's work
    def __save_tasks_json_file(self):
        json_data = self.task_list_view.model().prepare_model_for_json()
        with open("tasks.json", 'w') as file:
            json.dump(json_data, file, indent=4)

    # TODO: transforming model back to JSON to save in file
    # def model_to_json(self):
    #     json_result_data = []
    #     for task in self._tasks:
    #         json_result_data.append(task.serialize())
    #     return json_result_data

    def __open_jobs_json_file(self):
        with open("jobs.json", 'r') as file:
            json_data = json.load(file)
        self.job_list_view.model().prepare_json_for_model(json_data)

    def __save_json_jobs_file(self):
        json_data = self.job_list_view.model().prepare_model_for_json()
        with open("jobs.json", 'w') as file:
            json.dump(json_data, file, indent=4)

    def __save_to_files(self):
        self.__save_tasks_json_file()
        self.__save_json_jobs_file()

    def __start_task(self, index):
        if index.isValid():
            if not self._is_allowed_multiple_tasks_running:
                tasks = self.task_list_view.model().data(index, constants.getFullDataRole)
                if not any()     # TODO: FINISH

        if index.isValid():
            if not self._is_allowed_multiple_tasks_running:
                if self._currently_selected_entity_index is not None and not any([task.is_task_running() for task in self._tasks]):
                    self._tasks[self._currently_selected_entity_index].start_task()
                    self.task_list_view.update(index)
                    # self.update_task_view()
                else:
                    self.show_error_message()
            else:
                if self._currently_selected_entity_index is not None:
                    self._tasks[self._currently_selected_entity_index].start_task()
                    self.task_list_view.update(index)
                    # self.update_task_view()

    def __end_task(self, index):      # FIXME: only allow when task isRunning == True
        if index.isValid():
            self._tasks[self._currently_selected_entity_index].end_task()
            self.task_list_view.update(index)
            # self.update_task_view()

    def __on_task_switch(self, index):      # double click operator for task list view
        if index.isValid():
            if self.task_list_view.model().data(index, role=isTaskRunningRole) is False:
                self.__start_task(index)
            else:
                self.__end_task(index)

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
    def __on_edit_entity(view):
        pass

    # updating index of selected task
    def on_selection_changed(self):
        selection_model = self.task_list_view.selectionModel()
        selected_indexes = selection_model.selectedIndexes()
        for index in selected_indexes:
            # TODO: passing index, while having protected variable of selected task
            self._currently_selected_entity_index = index.row()
            # self.update_task_view()

    def update_task_view(self):
        current_task = self._tasks[self._currently_selected_entity_index].get_task("USER")
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
        error_dialog_box.setText("Not allowed running multiple tasks.")
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
        edit_action.triggered.connect(lambda: self.__on_edit_entity(view))

        if any(view.selectionModel().selectedIndexes()):
            context_menu.addAction(add_action)
            context_menu.addAction(delete_action)
            context_menu.addAction(rename_action)
            context_menu.addAction(edit_action)
        else:
            context_menu.addAction(add_action)

        context_menu.exec_(view.mapToGlobal(event))
