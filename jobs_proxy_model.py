import typing

from PyQt5.QtCore import QSortFilterProxyModel, QModelIndex, QVariant, Qt

import constants


class JobsProxyModel(QSortFilterProxyModel):
    def __init__(self, source_model):
        super(JobsProxyModel, self).__init__()
        self.setSourceModel(source_model)

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if not index.isValid():
            return QVariant()

        row = index.row()

        source_index = self.sourceModel().index(row, 0)

        data = self.sourceModel().data(source_index, constants.getJobRegisterDateRole)

        if role == Qt.DisplayRole:
            return data
