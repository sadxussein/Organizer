from PyQt5.QtCore import Qt, QModelIndex, QAbstractItemModel
from PyQt5.QtGui import QPainter, QPixmap, QColor
from PyQt5.QtWidgets import QStyledItemDelegate, QWidget, QStyleOptionViewItem, QLineEdit


# all function names are quite self explanatory
import constants


class TaskListDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(TaskListDelegate, self).__init__()

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QModelIndex) -> QWidget:
        editor = QLineEdit(parent)
        editor.setFrame(True)
        editor.setMaxLength(20)
        return editor

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        assert isinstance(editor, QLineEdit)
        value = index.model().data(index, Qt.EditRole)
        editor.setText(value)

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex) -> None:
        assert isinstance(editor, QLineEdit)
        value = editor.text()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor: QWidget, option: 'QStyleOptionViewItem', index: QModelIndex) -> None:
        editor.setGeometry(option.rect)

    def paint(self, painter: QPainter, option: 'QStyleOptionViewItem', index: QModelIndex) -> None:
        if index.isValid() and index.data(constants.isTaskRunningRole):
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 255, 0))
            painter.drawRect(option.rect)

            painter.setPen(Qt.black)
            painter.drawText(option.rect, Qt.AlignCenter, "Running")

            super().paint(painter, option, index)
        else:
            super().paint(painter, option, index)
