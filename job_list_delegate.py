from PyQt5.QtCore import QModelIndex, Qt, QAbstractItemModel
from PyQt5.QtWidgets import QStyledItemDelegate, QWidget, QLineEdit, QStyleOptionViewItem


class JobListDelegate(QStyledItemDelegate):
    def __init__(self):
        super(JobListDelegate, self).__init__()

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
