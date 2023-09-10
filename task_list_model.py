import typing

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant

import constants
from task import Task


class TaskListModel(QAbstractListModel):
    # default constructor
    def __init__(self, data=None):
        QAbstractListModel.__init__(self)
        # if data is None replace it with empty list, to safe myself from unnecessary checks
        # self._data = [task.get_task("NAME") for task in data] or []
        self._data = data or []
        print(data)

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

    # drag'n'drop flags
    # def supportedDragActions(self) -> Qt.DropActions:
    #     return Qt.CopyAction | Qt.MoveAction
    #
    # def supportedDropActions(self) -> Qt.DropActions:
    #     return Qt.CopyAction | Qt.MoveAction
