from timeit import timeit

from data.dot import TitleGenerator
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
        self.bind_buttons()
        self.ui.canvas.set_tb(self.ui.data_tb)

    def bind_buttons(self):
        self.ui.clear_data_button.clicked.connect(lambda: self.clear())
        self.ui.delay_draw_button.clicked.connect(
            lambda: self.draw_rastor(delay=True))
        self.ui.no_delay_draw_button.clicked.connect(
            lambda: self.draw_rastor())
        self.ui.lock_circuit_button.clicked.connect(
            lambda: self.ui.canvas.close_poly())

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
        self.ui.data_tb.clear()
        TitleGenerator.reset()

    def time_info(self, time):
        if time is not None:
            text = f'Время закраски: {round(time, 2)} мс'
        else:
            text = f'Время закраски: None'
        QtWidgets.QMessageBox.about(self, "Время", text)

    def draw_rastor(self, delay=False) -> None:
        color = self.get_curr_color()
        result = None
        if not delay:
            result = timeit(lambda: self.ui.canvas.fill(color, delay),
                            number=1) * 1000
            self.time_info(result)
        else:
            self.ui.canvas.fill(color, delay)
