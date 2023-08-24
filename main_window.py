from PyQt5.uic import loadUi
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QWidget
from task_table_model import TaskTableModel
import json


# TODO: create new task form
# TODO: connect them with calendar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # init JSON handling structure
        self.json_model = QStandardItemModel()
        self.table_model = TaskTableModel()
        # load UI file
        loadUi("main.ui", self)
        self.init_window()

    def init_window(self):
        # create JSON model for input file
        self.open_json_file()
        # use tree element created from UI
        # self.tree_view.setModel(self.json_model)
        self.table_view.setModel(self.table_model)
        self.save_file.clicked.connect(lambda: self.save_json_file(self.json_model))
        self.add_task.clicked.connect(lambda: self.on_add_task(self.json_model))
        self.delete_task.clicked.connect(lambda: self.on_delete_task(self.json_model))
        self.modify_task.clicked.connect(lambda: self.on_modify_task(self.json_model))

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
    def on_add_task(self, parent_item):
        print("added task")
        pass

    # delete task button function
    def on_delete_task(self, parent_item):
        print("deleted task")
        pass

    # modify task button function
    def on_modify_task(self, parent_item):
        print("modified task")
        pass
