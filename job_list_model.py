import typing

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant

from job import Job


class JobListModel(QAbstractListModel):
    def __init__(self, data=None):
        super(JobListModel, self).__init__()
        self._data = data or []
        # TODO: consider instance check

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid():
            return QVariant()

        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self._data[index.row()].get_job_name()

        return QVariant()

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if not index.isValid():
            return False

        if role == Qt.EditRole:
            self._data[index.row()].set_job_name(value)
            self.dataChanged.emit(index, index)
            return True

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self._data)

    def insertRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        for _ in range(count):
            self._data.insert(row, Job("No name job"))
        self.endInsertRows()
        return True

    def removeRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        self.beginRemoveRows(QModelIndex(), row, row + count - 1)
        for _ in range(count):
            del self._data[row]
        self.endRemoveRows()
        return True

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.ItemIsEnabled

        return super(JobListModel, self).flags(index) | Qt.ItemIsEditable
