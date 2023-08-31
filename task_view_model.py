import typing

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt


class TaskViewModel(QAbstractTableModel):
    def __init__(self):
        super(TaskViewModel, self).__init__()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return 4

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return 2
