from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel


class DateCategoryWidget(QWidget):
    def __init__(self, date):
        super(DateCategoryWidget, self).__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel(f"{date}")
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)