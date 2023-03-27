from PyQt5 import QtWidgets
from clipper import Clipper
from point import Point
from line import Line
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QImage, QPixmap
from PyQt5.QtWidgets import QLabel
from line_algos import dda


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
        if (self.ui.cutter_rb.isChecked()):
            self.add_clipper(self.start_point)
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.end_point = Point(event.pos().x(), event.pos().y())
        if (self.ui.ls_rb.isChecked()):
            if event.modifiers() == Qt.ControlModifier and \
                not self.clipper is None and self.clipper.len() > 1:
                edge = self.clipper.get_nearest_edge(self.start_point,
                                                     self.end_point)
                self.end_point = Line.make_parallel(edge, self.start_point,
                                                    self.end_point)
            self.add_line(self.start_point, self.end_point)
        return super().mouseReleaseEvent(event)

    def add_line(self, start: Point, end: Point) -> None:
        self.lines.append(Line(start, end))
        color = self.ui.ls_color_cb.get_qcolor()
        self.draw_line(self.lines[-1], color)
        self.image_set()

    def add_clipper(self, point: Point) -> None:
        if self.clipper is None:
            self.clipper = Clipper()
        if not self.clipper.is_empty() and self.clipper.is_locked():
            QtWidgets.QMessageBox.warning(
                self, "Ошибка",
                "Отсекатель уже задан и замкнут. Выполните очистку.")
            return
        self.clipper.add_point(point)
        color = self.ui.cutter_color_cb.get_qcolor()
        self.draw_clipper_last_seg(self.clipper, color)
        self.image_set()

    def clipper_lock(self):
        if self.clipper is None:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                                          "Отсекатель не задан.")
            return
        if self.clipper.len() < 3:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                                          "Не достаточно вершин отсекателя.")
            return
        if self.clipper.is_locked():
            QtWidgets.QMessageBox.warning(
                self, "Ошибка",
                "Отсекатель уже задан и замкнут. Выполните очистку.")
        else:
            self.add_clipper(self.clipper.first_p())

    def draw_clipper_last_seg(self, clipper: Clipper, color: QColor) -> None:
        if clipper.len() > 1:
            self.draw_line(Line(clipper.last_p(), clipper.pre_last_p()), color)
        else:
            self.draw_line(Line(clipper.last_p(), clipper.last_p()), color)

    def draw_line(self, line: Line, color: QColor) -> None:
        dda(self.image, line.start, line.end, color)

    def draw_lines(self, lines: list[Line], color) -> None:
        for line in lines:
            self.draw_line(line, color)

    def clip(self) -> None:
        if self.clipper is None:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                                          "Не задан отсекатель")
            return
        elif self.clipper.len() < 3:
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                                          "Не достаточно вершин отсекателя.")
            return
        elif not self.clipper.is_locked():
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                                          "Отсекатель не замкнут.")
            return
        elif not self.clipper.is_convex():
            QtWidgets.QMessageBox.warning(self, "Ошибка",
                                          "Отсекатель не выпуклый.")
            return
        
        self.result = self.clipper.clip_lines(self.lines)
        color = self.ui.result_color_cb.get_qcolor()
        
        self.draw_lines(self.result, color)
        self.image_set()

    def clear(self) -> None:
        self.clipper: Clipper = None
        self.lines: list[Line] = []
        self.image_init()
        self.image_set()
