import json

from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QMainWindow, QWidget, QAbstractItemView, QListView, QPushButton, QVBoxLayout, QTableView, \
    QScrollArea, QHBoxLayout, QLabel, QLineEdit

from task import Task
from task_list_model import TaskListModel
from task_view_model import TaskViewModel
from task_list_delegate import TaskListDelegate


# TODO: create new task form
# TODO: connect them with calendar
# TODO: create graphs for tasks
# TODO: create task groups, maybe even tags


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # meta variables
        self._currently_selected_task = None
        # elements of the window
        self.central_widget = QWidget(self)
        self.layout = QVBoxLayout()
        self.task_list_view = QListView()
        self.start_task_button = QPushButton("Start task")
        self.end_task_button = QPushButton("End task")
        self.task_view_scroll_area = QScrollArea()
        self.task_view_scroll_content = QWidget()
        self.task_view_layout = QVBoxLayout(self.task_view_scroll_content)
        self.task_view_element_pairs = []
        self.add_task_button = QPushButton("Add task")
        self.delete_task_button = QPushButton("Delete task")
        self.save_tasks_button = QPushButton("Save tasks")
        # models & loading data from JSON file
        self._tasks = []
        self.open_json_file()
        self._task_list_model = TaskListModel(self._tasks)
        self._task_list_view_selection_model = None
        # delegates
        self._task_list_delegate = TaskListDelegate()
        # initializing main elements of the window
        self.init_window()

    # setting up window's elements properties
    def init_window(self):
        # widget to which other elements are attached to
        self.setCentralWidget(self.central_widget)
        # all tasks in a list
        self.task_list_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.task_list_view.setDragEnabled(True)
        self.task_list_view.setAcceptDrops(True)
        self.task_list_view.setDropIndicatorShown(True)
        self.task_list_view.setModel(self._task_list_model)
        self.task_list_view.setItemDelegate(self._task_list_delegate)
        self._task_list_view_selection_model = self.task_list_view.selectionModel()
        self._task_list_view_selection_model.selectionChanged.connect(self.on_selection_changed)
        # control buttons

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
        self.add_task_button.clicked.connect(self.on_add_task)
        self.delete_task_button.clicked.connect(self.on_delete_task)
        self.save_tasks_button.clicked.connect(self.save_json_file)
        # adding elements to layout
        self.layout.addWidget(self.task_list_view)
        self.layout.addWidget(self.start_task_button)
        self.layout.addWidget(self.end_task_button)
        self.layout.addWidget(self.task_view_scroll_area)
        self.layout.addWidget(self.add_task_button)
        self.layout.addWidget(self.delete_task_button)
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
        # print("json", json_data) FIXME: remove debug
        self.json_to_models(self._tasks, json_data)

    # transforming JSON data to multiple models for views
    def json_to_models(self, parent_item, data):
        for el in data:
            self._tasks.append(Task(el["name"], el["registerTime"], el["isRunning"],
                                    el["startTime"], el["endTime"], el["timeRanges"]))

    # saving to file results of program's work
    def save_json_file(self, model):
        root = model.invisibleRootItem()
        json_data = self.model_to_json(root)
        with open("test.json", "w") as file:
            json.dump(json_data, file, indent=4)

    # transforming model back to JSON to save in file
    def model_to_json(self, parent_item):
        if parent_item.hasChildren():
            result = {}
            test_result = []
            for row in range(parent_item.rowCount()):
                print(parent_item.text(), parent_item.child(row).text())
                child_item = parent_item.child(row)
                test_result.append(child_item.text())
                result[child_item.text()] = self.model_to_json(child_item)
            print(test_result)
            return result
        else:
            return parent_item.text()

    # add task button function
    def on_add_task(self):
        rows = self._task_list_model.rowCount()
        self._tasks.append(Task("No name task"))
        print(self._tasks)
        self._task_list_model.insertRows(rows, 1)

    # delete task button function
    def on_delete_task(self):
        # TODO: rewrite for usage of _task_list_selection_model
        selection_model = self.task_list_view.selectionModel()
        selected_indexes = selection_model.selectedIndexes()
        # in case if in the future task list view will support multi-selection
        for index in selected_indexes:
            self._task_list_model.removeRows(index.row(), 1)
            del self._tasks[index.row()]
            # print(self._tasks) FIXME: remove debug

    def on_start_task(self):
        print(self._currently_selected_task)
        if self._currently_selected_task is not None:
            self._tasks[self._currently_selected_task].start_task()
            self.update_task_view()

    def on_end_task(self):
        print(self._currently_selected_task)
        if self._currently_selected_task is not None:
            self._tasks[self._currently_selected_task].end_task()
            self.update_task_view()

    # updating index of selected task
    def on_selection_changed(self):
        selection_model = self.task_list_view.selectionModel()
        selected_indexes = selection_model.selectedIndexes()
        for index in selected_indexes:
            # TODO: passing index, while having protected variable of selected task
            self._currently_selected_task = index.row()
            self.update_task_view()

    def update_task_view(self):
        # print(f"Selected item under index {self._currently_selected_task}")   # FIXME: remove debug
        current_task = self._tasks[self._currently_selected_task].get_task("JSON")
        print(len(current_task))  # FIXME: remove debug
        print(current_task)         # FIXME: remove debug
        for i in range(len(current_task)):
            self.task_view_element_pairs[i][1].setText(f"{current_task[i]}")

