import json

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QWidget, QListView, QPushButton, QVBoxLayout, \
    QScrollArea, QHBoxLayout, QLabel, QLineEdit, QAction, QMessageBox, QTabWidget, QMenu

import constants
from constants import isTaskRunningRole
from entity_list_view import EntityListView
from graph_widget import GraphWidget
from job import Job
from job_list_delegate import JobListDelegate
from job_list_model import JobListModel
from task import Task
from task_list_model import TaskListModel
from task_list_delegate import TaskListDelegate
from task_ordered_model import TaskOrderedModel


# TODO: connect them with calendar
# TODO: create graphs for tasks
# TODO: create task groups, maybe even tags
# TODO: try visualize tasks as icons in list view
# TODO: make one-time tasks subsidiary of tasks
# TODO: create options class
# TODO: create detailed list view for both jobs and tasks


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # meta variables
        self._currently_selected_entity_index = None
        self._currently_selected_job = None
        self._is_allowed_multiple_tasks_running = False
        self._is_single_task_running = False    # TODO: initialise this based on loaded json files
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
        # tabs and graphs layout
        self.top_layout = QHBoxLayout()
        self.top_widget = QWidget(self)
        # tabs
        self.tab_widget = QTabWidget(self)
        self.task_list_view_widget = QWidget()
        self.task_list_view = EntityListView(self.task_list_view_widget)
        self.task_ordered_view_widget = QWidget()
        self.task_ordered_view = EntityListView(self.task_ordered_view_widget)
        # self.task_graph_view_widget = QWidget()
        # self.task_graph_view = QListView(self.task_graph_view_widget)      # TODO: use proper view for drawing graphs
        self.job_list_view_widget = QWidget()
        self.job_list_view = EntityListView(self.job_list_view_widget)
        # graph view
        self.graph_view = GraphWidget()
        self.bottom_widget = QWidget(self)
        # task and job detailed layout
        self.bottom_layout = QHBoxLayout()      # TODO: consider renaming
        # task and job detailed list view
        self.detailed_entity_view = QListView(self)
        self.time_ranges_view = QListView(self)     # TODO: consider renaming
        # save button
        self.save_button = QPushButton("Save")
        # models & loading data from JSON file
        self._tasks = []
        self._jobs = []
        self._task_list_model = TaskListModel(self._tasks)      # TODO: why constructor has argument?
        self._task_list_view_selection_model = None
        self.__task_ordered_model = TaskOrderedModel()
        self._job_list_model = JobListModel(self._jobs)
        self._job_list_view_selection_model = None
        self.__detailed_entity_model = QStandardItemModel()
        self.__time_ranges_model = QStandardItemModel()
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
        self.task_list_view.doubleClicked.connect(lambda index: self.__on_task_switch(index))
        self._task_list_view_selection_model = self.task_list_view.selectionModel()
        self._task_list_view_selection_model.selectionChanged.connect(lambda: self.__on_selection_changed(self.task_list_view))
        # task ordered view
        self.task_ordered_view.setModel(self.__task_ordered_model)
        # TODO: task graph view
        # job list view
        self.job_list_view.setModel(self._job_list_model)
        self.job_list_view.setItemDelegate(self._job_list_delegate)
        self.job_list_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.job_list_view.customContextMenuRequested.connect(lambda event: self.show_context_menu(event, self.job_list_view))
        self._job_list_view_selection_model = self.job_list_view.selectionModel()
        self._job_list_view_selection_model.selectionChanged.connect(lambda: self.__on_selection_changed(self.job_list_view))
        # detailed entity view
        self.detailed_entity_view.setEditTriggers(QListView.NoEditTriggers)
        self.detailed_entity_view.setModel(self.__detailed_entity_model)
        self.time_ranges_view.setEditTriggers(QListView.NoEditTriggers)
        self.time_ranges_view.setModel(self.__time_ranges_model)
        # save button
        self.save_button.clicked.connect(self.__save_to_files)
        # adding elements to tab layout
        self.tab_widget.addTab(self.task_list_view, "Task list")
        self.tab_widget.addTab(self.task_ordered_view, "Ordered task list")
        # self.tab_widget.addTab(self.task_graph_view, "Task graph")           # TODO: consider removal
        self.tab_widget.addTab(self.job_list_view, "Job list")
        # adding elements to top layout (entity list view and graph view)
        self.top_layout.addWidget(self.tab_widget)
        self.top_layout.addWidget(self.graph_view)
        self.top_layout.setStretchFactor(self.tab_widget, 1)
        self.top_layout.setStretchFactor(self.graph_view, 1)
        self.top_widget.setLayout(self.top_layout)
        # adding elements to bottom layout (detailed entity view and time ranges view)
        self.bottom_layout.addWidget(self.detailed_entity_view)
        self.bottom_layout.addWidget(self.time_ranges_view)
        self.bottom_widget.setLayout(self.bottom_layout)
        # adding elements to main layout
        self.layout.addWidget(self.top_widget)
        self.layout.addWidget(self.bottom_widget)
        self.layout.addWidget(self.save_button)
        # applying layout to central widget
        self.central_widget.setLayout(self.layout)
        # window size
        self.setGeometry(200, 200, 800, 800)

    # opening file and extracting data
    def __open_tasks_json_file(self):
        with open("tasks.json", 'r') as file:   # JSON file containing our tasks
            json_data = json.load(file)         # store all our tasks which now need to be parsed into simple list
        # import from file into model
        self.task_list_view.model().prepare_json_for_model(json_data)
        self.task_ordered_view.model().prepare_json_for_model(json_data)

    # TODO: saving to file results of program's work
    def __save_tasks_json_file(self):
        json_data = self.task_list_view.model().prepare_model_for_json()
        with open("tasks.json", 'w') as file:
            json.dump(json_data, file, indent=4)

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
                is_selected_task_running = self.task_list_view.model().data(index, constants.isTaskRunningRole)
                if not is_selected_task_running and not self._is_single_task_running:
                    self.task_list_view.model().setData(index, value=None, role=constants.startTaskRole)
                    self._is_single_task_running = True
                else:
                    self.show_error_message()

    def __end_task(self, index):      # FIXME: only allow when task isRunning == True
        if index.isValid():
            is_selected_task_running = self.task_list_view.model().data(index, constants.isTaskRunningRole)
            if is_selected_task_running and self._is_single_task_running:
                self.task_list_view.model().setData(index, value=None, role=constants.endTaskRole)
                self._is_single_task_running = False

    def __on_task_switch(self, index):      # double click operator for task list view
        if index.isValid():
            # TODO: might be overkill, checking is_running again inside start function
            if self.task_list_view.model().data(index, role=isTaskRunningRole) is False:
                self.__start_task(index)
            else:
                self.__end_task(index)
            self.__on_selection_changed(self.task_list_view)

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
    def __on_selection_changed(self, view):
        for index in view.selectionModel().selectedIndexes():
            # TODO: passing index, while having protected variable of selected task
            self._currently_selected_entity_index = index
            self.__update_detailed_entity_views(view, index)

    # TODO: need to think about this logic, it might be necessary to save application status of options to prevent
    #   multiple tasks running when it is not allowed after loading
    def on_allow_multiple_tasks_running(self):
        if self._is_allowed_multiple_tasks_running:
            self._is_allowed_multiple_tasks_running = False
        else:
            self._is_allowed_multiple_tasks_running = True

    def __update_detailed_entity_views(self, view, index):  # both detailed view and time ranges view
        if isinstance(view, EntityListView):
            self.__detailed_entity_model.clear()
            self.__time_ranges_model.clear()
            model = view.model()
            if isinstance(model, TaskListModel):
                task_data = model.data(index, constants.getSingleEntityRole)
                task_data = task_data.serialize()
                for key, value in task_data.items():
                    if key == "timeRanges" and value is not None:
                        for el in value:
                            task_item = QStandardItem(f"{key}: {el}")
                            self.__time_ranges_model.appendRow(task_item)
                    else:
                        task_item = QStandardItem(f"{key}: {value}")
                        self.__detailed_entity_model.appendRow(task_item)
            elif isinstance(model, JobListModel):
                job_data = model.data(index, constants.getSingleEntityRole)
                job_data = job_data.serialize()
                for key, value in job_data.items():
                    job_item = QStandardItem(f"{key}: {value}")
                    self.__detailed_entity_model.appendRow(job_item)

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
