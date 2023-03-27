from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from interface import Ui_MainWindow
from point import Point


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui_setup()

    def ui_setup(self) -> None:
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        self.ui.canvas.image_init()
        self.ui.canvas.image_set()
        self.ui.canvas.ui_set(self.ui)
        self.bind_buttons()

    def bind_buttons(self):
        self.ui.clear_button.clicked.connect(lambda: self.clear())
        self.ui.ls_add_button.clicked.connect(lambda: self.line_processing())
        self.ui.cutter_lock_button.clicked.connect(lambda: self.clipper_lock())
        self.ui.cutter_add_button.clicked.connect(
            lambda: self.clipper_processing())
        self.ui.perform_button.clicked.connect(lambda: self.perform())

    def line_processing(self):
        start = Point(self.ui.ls_x0_sb.value(), self.ui.ls_y0_sb.value())
        end = Point(self.ui.ls_x1_sb.value(), self.ui.ls_y1_sb.value())
        self.ui.canvas.add_line(start, end)

    def clipper_processing(self):
        point = Point(self.ui.cutter_xmin_sb.value(),
                      self.ui.cutter_ymin_sb.value())
        self.ui.canvas.add_clipper(point)

    def clipper_lock(self):
        self.ui.canvas.clipper_lock()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.ui.canvas.clear()
        return super().resizeEvent(event)

    def clear(self):
        self.ui.canvas.clear()

    def perform(self):
        self.ui.canvas.clip()
