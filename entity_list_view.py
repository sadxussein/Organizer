from PyQt5 import QtGui
from PyQt5.QtWidgets import QListView


class EntityListView(QListView):
    def __init__(self, parent):
        super(EntityListView, self).__init__(parent)

    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        index = self.indexAt(e.pos())
        if not index.isValid():
            self.clearSelection()
        super(EntityListView, self).mousePressEvent(e)
