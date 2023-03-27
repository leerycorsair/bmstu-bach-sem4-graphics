from data.dot import Dot
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from interface import Ui_MainWindow


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui_setup()

    def ui_setup(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        self.ui.canvas.image_init()
        self.ui.canvas.image_set()
        self.ui.canvas.set_ui(self.ui)
        self.ui.canvas.set_main_w(self)
        self.bind_buttons()

    def bind_buttons(self):
        self.ui.clear_data_button.clicked.connect(lambda: self.clear())
        self.ui.lock_circuit_button.clicked.connect(
            lambda: self.ui.canvas.close_poly())
        self.ui.draw_button.clicked.connect(lambda: self.draw())
        self.ui.add_dot_button.clicked.connect(lambda: self.add_dot())

    def draw(self):
        position = Dot(self.ui.x_z_sb.value(), self.ui.y_z_sb.value())
        if self.ui.draw_delay_rb.isChecked():
            self.ui.canvas.draw(position, delay=True)
        if self.ui.draw_no_delay_rb.isChecked():
            self.ui.canvas.draw(position)
    
    def add_dot(self):
        position = Dot(self.ui.x_dot_sb.value(), self.ui.y_dot_sb.value())
        self.ui.canvas.add_dot(position)

    def get_curr_color(self):
        if self.ui.white_rb.isChecked():
            return Qt.white
        if self.ui.blue_rb.isChecked():
            return Qt.blue
        if self.ui.green_rb.isChecked():
            return Qt.green
        if self.ui.red_rb.isChecked():
            return Qt.red

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.ui.canvas.image_init()
        self.ui.canvas.image_set()
        return super().resizeEvent(event)

    def clear(self):
        self.ui.canvas.clear()
