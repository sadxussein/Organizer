import typing

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt


class TaskListModel(QAbstractListModel):
    def __init__(self, data=None, prepared_data=None):
        QAbstractListModel.__init__(self)
        self._data = data or []
        self._prepared_data = "Set task name"

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data)

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid():
            return None

        row = index.row()
        if role == Qt.DisplayRole:
            return self._data[row]

    # TODO: is it really necessary?
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        pass

    def insertRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        if self._prepared_data is not None:
            self._data.insert(row, self._prepared_data)
        self.endInsertRows()
        # self.dataChanged.emit(self.index(row, 0), self.index(row + count - 1, 0))
        return True

    def removeRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        self.beginRemoveRows(QModelIndex(), row, row + count - 1)
        del self._data[row]
        self.endInsertRows()
        return True

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:

        return True

    def prepare_data(self, prepared_data):
        self._prepared_data = prepared_data
