import sys

from PyQt5.QtWidgets import QApplication

from main_window import MainWindow


# GUI
# TODO: detailed task view
# TODO: task groups, task tags
# TODO: consider loading not all tasks at once, since it may take too much space and time after and while loading


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
