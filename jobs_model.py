import typing
from datetime import datetime

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, QVariant

import constants
from job import Job


class JobsModel(QAbstractListModel):
    def __init__(self, data=None):
        super(JobsModel, self).__init__()
        self.__data = data or []
        self.headers = ["name", "registerDate", "parentTask", "endTime"]        # TODO: consider removal
        # TODO: consider instance check

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid():
            return QVariant()

        row = index.row()

        if role == Qt.DisplayRole or role == Qt.EditRole:
            if self.__data is not None:
                return self.__data[row].get_job_name()
        elif role == constants.getSingleEntityRole:
            return self.__data[row]
        elif role == constants.getJobRegisterDateRole:
            return self.__data[row].get_job_register_date()

        return QVariant()

    def setData(self, index: QModelIndex, value: typing.Any, role: int = ...) -> bool:
        if not index.isValid():
            return False

        row = index.row()

        if role == Qt.EditRole:
            self.__data[row].set_job_name(value)
            self.dataChanged.emit(index, index)
            return True

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.__data)

    def insertRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        # TODO: force user to name job after creating
        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        for _ in range(count):
            self.__data.insert(row, Job(""))
        self.endInsertRows()
        return True

    def removeRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        self.beginRemoveRows(QModelIndex(), row, row + count - 1)
        for _ in range(count):
            del self.__data[row]
        self.endRemoveRows()
        return True

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.ItemIsEnabled

        return super(JobsModel, self).flags(index) | Qt.ItemIsEditable

    def prepare_json_for_model(self, jobs):     # when opening file or starting application
        for job in jobs:
            self.__data.append(Job(job["name"], job["endTime"], job["parentTask"], job["registerDate"]))

    def prepare_model_for_json(self):       # when saving file TODO: implement saving on closing
        json_export = []
        for job in self.__data:
            json_export.append(job.serialize())
        return json_export
