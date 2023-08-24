import typing

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt


class TaskListModel(QAbstractListModel):
    def __init__(self, data=None):
        super().__init__(self)
        self._data = data

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data)

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        pass

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        pass

    def insertRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        self.beginInsertRows(QModelIndex(), row, row)
        self._data.insert(row, parent)
        self.endInsertRows()
        return True

    def removeRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        self.beginRemoveRows(QModelIndex(), row, row)
        del self._data[row]
        self.endInsertRows()
        return True
