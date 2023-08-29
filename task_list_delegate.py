from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyledItemDelegate, QWidget, QStyleOptionViewItem, QLineEdit


# all function names are quite self explanatory
class TaskListDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(TaskListDelegate, self).__init__()

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> QWidget:
        editor = QLineEdit(parent)
        editor.setFrame(False)
        editor.setMaxLength(20)
        return editor

    def setEditorData(self, editor: QWidget, index: QtCore.QModelIndex) -> None:
        assert isinstance(editor, QLineEdit)
        value = index.model().data(index, Qt.EditRole)
        editor.setText(value)

    def setModelData(self, editor: QWidget, model: QtCore.QAbstractItemModel, index: QtCore.QModelIndex) -> None:
        assert isinstance(editor, QLineEdit)
        value = editor.text()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor: QWidget, option: 'QStyleOptionViewItem', index: QtCore.QModelIndex) -> None:
        editor.setGeometry(option.rect)
