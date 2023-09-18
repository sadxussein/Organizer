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
        radial_gradient = QRadialGradient(100, 100, 50)
        radial_gradient.setColorAt(0, QColor(255, 0, 0))
        radial_gradient.setColorAt(0.5, QColor(0, 255, 0))
        radial_gradient.setColorAt(1, QColor(0, 0, 255))
        painter.setBrush(QBrush(radial_gradient))
        painter.drawEllipse(50, 50, 100, 100)

        # rectangular
        # painter.setPen(QPen(QColor(0, 0, 0), 2, Qt.SolidPattern))
        # painter.setBrush(QBrush(Qt.))
        painter.drawRect(200, 50, 100, 100)
