from PyQt5.QtCore import QSortFilterProxyModel, QModelIndex


class JobListProxyModel(QSortFilterProxyModel):
    def __init__(self, start_column, end_column):
        super(JobListProxyModel, self).__init__()
        self.start_column = start_column
        self.end_column = end_column

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        source_index = self.sourceModel().index()

        for column in range(self.start_column, self.end_column + 1):
            index = source_index.sibling(source_row, column)
            data = self.sourceModel().data(index, role=self.filterRole())

        return True
    