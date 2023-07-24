from PyQt5.uic import loadUi
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow
import json


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # load UI file
        loadUi("main.ui", self)
        self.init_window()

    def init_window(self):
        # create JSON model for input file
        with open("tasks.json", 'r') as file:   # JSON file containing our tasks
            json_data = json.load(file)         # store all our tasks which now need to be parsed into simple list
        json_model = QStandardItemModel()
        # import from file into model
        self.import_json_file(json_model, json_data)
        # use tree element created from UI
        self.treeView.setModel(json_model)

    # recursively adding data from nodes to tree view
    def import_json_file(self, parent_item, data):
        if isinstance(data, dict):
            for key, value in data.items():
                key_item = QStandardItem(str(key))
                parent_item.appendRow(key_item)
                self.import_json_file(key_item, value)
        elif isinstance(data, list):
            for value in data:
                self.import_json_file(parent_item, value)
        else:
            value_item = QStandardItem(str(data))
            parent_item.appendRow(value_item)
