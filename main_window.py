from PyQt5.QtCore import QDir
from PyQt5.uic import loadUi
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QWidget, QFileSystemModel
from task_table_model import TaskTableModel
from task_list_model import TaskListModel
import json


# TODO: create new task form
# TODO: connect them with calendar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # init JSON handling structure
        self.json_model = QStandardItemModel()
        # self._table_model = TaskTableModel()
        self._list_model = TaskListModel()
        self._file_model = QFileSystemModel()
        self._file_model.setRootPath(QDir.currentPath())
        # TODO: consider removing loading UI file
        loadUi("main.ui", self)
        self.init_window()

    def init_window(self):
        # create JSON model for input file
        # self.open_json_file()
        # use tree element created from UI
        # self.table_view.setModel(self._table_model)
        self.list_view.setModel(self._list_model)
        # self.list_view.setRootIndex(self._file_model.index(QDir.currentPath()))
        # self.save_file.clicked.connect(lambda: self.save_json_file(self.json_model))
        self.add_task.clicked.connect(self.on_add_task)
        # self.delete_task.clicked.connect(self.on_delete_task)
        # self.modify_task.clicked.connect(lambda: self.on_modify_task(self.json_model))
        # self.list_view.doubleClicked.connect(lambda: self.on_element_double_click(self._list_model))

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
        rows = self._list_model.rowCount(self.list_view)
        self._list_model.insertRows(rows, 1)
        print("added task")
        pass

    # delete task button function
    def on_delete_task(self, parent_item):
        rows = self._list_model.rowCount(self.list_view)
        self._list_model.removeRows(rows, 1)
        print("deleted task")
        pass

    # modify task button function
    def on_modify_task(self, parent_item):
        print("modified task")
        pass

    def on_element_double_click(self, parent_item):
        print("double_clicked")
