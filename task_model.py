import typing

from PyQt5.QtCore import QAbstractItemModel, QModelIndex


class TaskModel(QAbstractItemModel):
    def __init__(self, data=None):
        super(TaskModel, self).__init__()
        self._data = data or []

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        pass

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        pass

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        pass

    def insertRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        self.beginInsertRows(QModelIndex(), row, row + count - 1)

        self.endInsertRows()
        return True

    def removeRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        self.beginRemoveRows(QModelIndex(), row, row + count - 1)
        for el in range(count):
            del self._data[row]
        self.endRemoveRows()
        return True

    def insertColumns(self, column: int, count: int, parent: QModelIndex = ...) -> bool:
        self.beginInsertColumns(QModelIndex(), column, column + count - 1)  # TODO: need to read more about columns

        self.endInsertColumns()
        return True

    def removeColumns(self, column: int, count: int, parent: QModelIndex = ...) -> bool:
        self.beginRemoveColumns(QModelIndex(), column, column + count - 1)  # TODO: need to read more about columns
        for el in range(count):
            del self._data[column]
        self.endRemoveColumns()
        return True
