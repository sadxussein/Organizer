import json

from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QMainWindow, QWidget, QAbstractItemView, QListView, QPushButton, QVBoxLayout, QTableView

from task_list_model import TaskListModel
from task_view_model import TaskViewModel
from task_list_delegate import TaskListDelegate


# TODO: create new task form
# TODO: connect them with calendar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # main elements of the window
        self.central_widget = QWidget(self)
        self.task_list_view = QListView()
        self.task_view = QTableView()
        self.add_task_button = QPushButton("Add task")
        self.delete_task_button = QPushButton("Delete task")
        self.save_tasks_button = QPushButton("Save tasks")
        self.layout = QVBoxLayout()
        # models
        self._initial_data = ["Eat", "Sleep", "Fuck", "Repeat"]
        self._task_list_model = TaskListModel(self._initial_data)
        self._task_view_model = QStandardItemModel(4, 2, self.task_view)
        # delegates
        self._task_list_delegate = TaskListDelegate()
        # initializing main elements of the window
        self.init_window()

    # setting up window's elements properties
    def init_window(self):
        # widget to which other elements are attached to
        self.setCentralWidget(self.central_widget)
        # all tasks in a list
        self.task_list_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.task_list_view.setDragEnabled(True)
        self.task_list_view.viewport().setAcceptDrops(True)
        self.task_list_view.setDropIndicatorShown(True)
        self.task_list_view.setModel(self._task_list_model)
        self.task_list_view.setItemDelegate(self._task_list_delegate)
        # task detailed view
        self.task_view.horizontalHeader().setVisible(False)
        self.task_view.verticalHeader().setVisible(False)
        # self.task_view.
        self.task_view.setModel(self._task_view_model)
        # buttons, names are self explanatory
        self.add_task_button.clicked.connect(self.on_add_task)
        self.delete_task_button.clicked.connect(self.on_delete_task)
        self.save_tasks_button.clicked.connect(self.save_json_file)
        # adding elements to layout
        self.layout.addWidget(self.task_list_view)
        self.layout.addWidget(self.task_view)
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
        self.json_to_model(self.json_model, json_data)

    # transforming JSON to QStandardItemModel
    # recursively adding data from nodes to tree view
    def json_to_model(self, parent_item, data):
        if isinstance(data, dict):
            for key, value in data.items():
                key_item = QStandardItem(str(key))
                parent_item.appendRow(key_item)
                self.json_to_model(key_item, value)
        elif isinstance(data, list):
            for value in data:
                self.json_to_model(parent_item, value)
        else:
            value_item = QStandardItem(str(data))
            parent_item.appendRow(value_item)

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
        rows = self._task_list_model.rowCount(self._task_list_model)
        self._task_list_model.insertRows(rows, 1)

    # delete task button function
    def on_delete_task(self):
        # TODO: rewrite for usage of _task_list_selection_model
        selection_model = self.task_list_view.selectionModel()
        selected_indexes = selection_model.selectedIndexes()
        # in case if in the future task list view will support multi-selection
        for index in selected_indexes:
            self._task_list_model.removeRows(index.row(), 1)

    # updating index of selected task
    def on_selection_changed(self):
        selection_model = self.task_list_view.selectionModel()
        selected_indexes = selection_model.selectedIndexes()
        for index in selected_indexes:
            print(f"Selected item under index {index.row()}")
