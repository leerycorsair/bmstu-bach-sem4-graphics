from PyQt5 import QtCore, QtWidgets


class ColorBox(QtWidgets.QComboBox):
    def __init__(self, parent):
        super().__init__(parent)

    def get_qcolor(self):
        if self.currentIndex() == 0:
            return QtCore.Qt.black
        elif self.currentIndex() == 1:
            return QtCore.Qt.white
        elif self.currentIndex() == 2:
            return QtCore.Qt.red
        elif self.currentIndex() == 3:
            return QtCore.Qt.green
        elif self.currentIndex() == 4:
            return QtCore.Qt.blue
        elif self.currentIndex() == 5:
            return QtCore.Qt.yellow