from PyQt5.QtCore import QAbstractItemModel


# TODO: consider removal, might be unnecessary
class TaskModel(QAbstractItemModel):
    def __init__(self):
        super(TaskModel, self).__init__()
