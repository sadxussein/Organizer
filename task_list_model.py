import typing

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant


class TaskListModel(QAbstractListModel):
    def __init__(self, data=None, prepared_data=None):
        QAbstractListModel.__init__(self)
        self._data = data or []
        self._prepared_data = "Set task name"

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data)

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid():
            return QVariant()

        if role == Qt.DisplayRole or role == Qt.EditRole:
            # print("role == Qt.DisplayRole or role == Qt.EditRole")
            return self._data[index.row()]

        return QVariant()

    # TODO: is it really necessary?
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        pass

    def insertRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        if self._prepared_data is not None:
            self._data.insert(row, self._prepared_data)
        self.endInsertRows()
        return True

    def removeRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        self.beginRemoveRows(QModelIndex(), row, row + count - 1)
        del self._data[row]
        self.endRemoveRows()
        return True

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if index.isValid() and role == Qt.EditRole:
            self._data[index.row()] = value
            self.dataChanged.emit(index, index)
            print("TRUE")
            return True
        print("FALSE")
        return False

    # TODO: necessary?
    # def flags(self, index: QModelIndex) -> Qt.ItemFlags:
    #     return Qt.ItemIsEditable

    def prepare_data(self, prepared_data):
        self._prepared_data = prepared_data
