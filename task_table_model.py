import typing

from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt5.QtGui import QColor


class TaskTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        QAbstractTableModel.__init__(self)
        self.column_count = 3
        self.row_count = 8

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return self.row_count

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return self.column_count

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            print("display role selected", row, column)
            return None     # TODO: fix
        elif role == Qt.BackgroundRole:
            print("background role selected", row, column)
            return None     # TODO: fix
        elif role == Qt.TextAlignmentRole:
            print("text alignment role selected", row, column)
            return None     # TODO: fix

        return None
