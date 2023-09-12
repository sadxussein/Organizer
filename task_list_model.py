import typing

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant

import constants
from task import Task


class TaskListModel(QAbstractListModel):
    # default constructor
    def __init__(self, data=None):
        QAbstractListModel.__init__(self)
        self._data = data or []

    # implementing from parent class
    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data)

    # returning item of the data that corresponds to the index argument, by certain role
    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid():
            return QVariant()
        if index.row() >= len(self._data):
            return QVariant()

        if role == Qt.DisplayRole:
            return self._data[index.row()].get_task_name()
        elif role == Qt.EditRole:
            return self._data[index.row()].get_task_name()
        elif role == constants.isTaskRunningRole:
            return self._data[index.row()].is_task_running()
        elif role == constants.getFullDataRole:
            return self._data

        return QVariant()

    # editing data
    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if not index.isValid():
            return False

        if role == Qt.EditRole:
            self._data[index.row()].set_task_name(value)
            self.dataChanged.emit(index, index)
            return True

        return False

    # setting flags for data in model and view to become editable
    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.ItemIsEnabled     # | Qt.ItemIsDropEnabled

        return super().flags(index) | Qt.ItemIsEditable     # | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled

    # adding empty task to model
    def insertRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        for el in range(count):
            self._data.insert(row, Task("No name task"))
        self.endInsertRows()
        return True

    # removing selected task from model
    def removeRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        self.beginRemoveRows(QModelIndex(), row, row + count - 1)
        for el in range(count):
            del self._data[row]
        self.endRemoveRows()
        return True

    def prepare_json_for_model(self, data):
        for el in data:
            self._data.append(Task(el["name"], el["registerTime"], el["isRunning"],
                                   el["startTime"], el["endTime"], el["timeRanges"]))

    def prepare_model_for_json(self):
        json_export = []
        for el in self._data:
            json_export.append(el.serialize())
        return json_export
