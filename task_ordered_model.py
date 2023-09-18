from datetime import datetime
import typing

from PyQt5.QtCore import QAbstractListModel, QModelIndex, QVariant, Qt


class TaskOrderedModel(QAbstractListModel):
    def __init__(self):
        super(TaskOrderedModel, self).__init__()
        self.__data = []

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid():
            return QVariant()

        if role == Qt.DisplayRole:
            return str(self.__data[index.row()][0] + ' ' + self.__data[index.row()][1])

        return QVariant()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.__data)

    def prepare_json_for_model(self, json_data):
        print(json_data)
        for task in json_data:
            if task["timeRanges"] is not None:
                for time_range in task["timeRanges"]:
                    print(time_range)
                    self.__data.append(time_range)
