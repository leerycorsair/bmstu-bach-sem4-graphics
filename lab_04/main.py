from PyQt5 import QtWidgets
import sys
import my_window

if (__name__ == "__main__"):
    app = QtWidgets.QApplication([])
    application = my_window.mywindow()
    sys.exit(app.exec())