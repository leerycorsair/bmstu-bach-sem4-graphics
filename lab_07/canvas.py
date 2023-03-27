from PyQt5 import QtGui
from PyQt5 import QtWidgets
from line_algos import dda
from point import Point
from line import Line
from clipper import Clipper
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QImage, QPainter, QPixmap
from PyQt5.QtWidgets import QLabel


class Canvas(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.clipper: Clipper = None
        self.lines: list[Line] = []

    def image_init(self) -> None:
        self.image = QImage(self.width(), self.height(),
                            QImage.Format_ARGB32_Premultiplied)
        self.image.fill(Qt.white)

    def image_set(self) -> None:
        self.pixmap = QPixmap().fromImage(self.image)
        self.setPixmap(self.pixmap)

    def ui_set(self, ui) -> None:
        self.ui = ui

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        self.start_point = Point(event.pos().x(), event.pos().y())
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.end_point = Point(event.pos().x(), event.pos().y())
        if (self.ui.ls_rb.isChecked()):
            self.add_line(self.start_point, self.end_point)
        else:
            self.add_clipper(self.start_point, self.end_point)
        return super().mouseReleaseEvent(event)

    def add_line(self, start: Point, end: Point) -> None:
        self.lines.append(Line(start, end))
        color = self.ui.ls_color_cb.get_qcolor()
        self.draw_line(self.lines[-1], color)
        self.image_set()

    def add_clipper(self, start: Point, end: Point) -> None:
        self.image_init()
        color = self.ui.ls_color_cb.get_qcolor()
        self.draw_lines(self.lines, color)
        self.clipper = Clipper(min(start.x, end.x), max(start.x, end.x),
                               min(start.y, end.y), max(start.y, end.y))
        self.draw_clipper(self.clipper)
        self.image_set()

    def draw_line(self, line: Line, color: QColor) -> None:
        dda(self.image, line.start, line.end, color)

    def draw_lines(self, lines: list[Line], color):
        for line in lines:
            self.draw_line(line, color)

    def draw_clipper(self, clipper: Clipper) -> None:
        color = self.ui.cutter_color_cb.get_qcolor()
        dda(self.image, Point(clipper.x_left, clipper.y_bottom),
            Point(clipper.x_right, clipper.y_bottom), color)
        dda(self.image, Point(clipper.x_right, clipper.y_bottom),
            Point(clipper.x_right, clipper.y_top), color)
        dda(self.image, Point(clipper.x_right, clipper.y_top),
            Point(clipper.x_left, clipper.y_top), color)
        dda(self.image, Point(clipper.x_left, clipper.y_top),
            Point(clipper.x_left, clipper.y_bottom), color)

    def clear(self) -> None:
        self.clipper: Clipper = None
        self.lines: list[Line] = []
        self.image_init()
        self.image_set()

    def fill_clipper(self):
        for x in range(self.clipper.x_left+1, self.clipper.x_right):
            for y in range(self.clipper.y_bottom+1,self.clipper.y_top):
                self.image.setPixelColor(x, y, Qt.white)

    def clip(self) -> None:
        if self.clipper is None:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                                          "Не задан отсекатель")
        self.fill_clipper()
        self.result = self.clipper.clip_lines(self.lines)
        color = self.ui.result_color_cb.get_qcolor()
        self.draw_lines(self.result, color)
        self.image_set()