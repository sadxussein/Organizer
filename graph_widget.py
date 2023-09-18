from PyQt5 import QtGui, Qt
from PyQt5.QtGui import QPainter, QRadialGradient, QColor, QBrush, QPen
from PyQt5.QtWidgets import QWidget


class GraphWidget(QWidget):     # TODO: create graphs
    def __init__(self):
        super(GraphWidget, self).__init__()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # radial
        painter.drawEllipse(50, 50, 100, 100)

        # rectangular
        painter.drawRect(200, 50, 100, 100)
