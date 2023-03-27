from line_algos import dda
from data.dot import Dot
from data.figure import Figure
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QImage, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel
import utils
from timeit import timeit
from PyQt5 import QtWidgets


class Canvas(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.figure = Figure()

    def image_init(self):
        self.image = QImage(self.width(), self.height(),
                            QImage.Format_ARGB32_Premultiplied)
        self.image.fill(Qt.white)

    def image_set(self):
        self.pixmap = QPixmap().fromImage(self.image)
        self.setPixmap(self.pixmap)

    def set_ui(self, ui):
        self.ui = ui

    def set_main_w(self, w):
        self.mw = w

    def clear(self):
        self.figure.clear()
        self.image_init()
        self.image_set()

    def mousePressEvent(self, event) -> None:
        position = Dot(event.pos().x(), event.pos().y())
        if self.ui.draw_circuit_rb.isChecked():
            if event.buttons() == Qt.LeftButton:
                exactly = QApplication.keyboardModifiers() & Qt.ControlModifier
                self.add_dot(position, exactly=exactly)
            elif event.buttons() == Qt.RightButton:
                self.close_poly()
        else:
            if self.ui.draw_delay_rb.isChecked():
                self.draw(position, delay=True)
            else:
                self.draw(position)

    def mouseMoveEvent(self, event) -> None:
        if self.ui.draw_circuit_rb.isChecked():
            position = Dot(event.pos().x(), event.pos().y())
            if event.buttons() == Qt.LeftButton:
                exactly = QApplication.keyboardModifiers() & Qt.ControlModifier
                self.add_dot(position, exactly=exactly)

    def draw(self, seed: Dot, delay=False):
        color = self.mw.get_curr_color()
        result = None
        if not delay:
            result = timeit(lambda: self.fill(seed, color, delay),
                            number=1) * 1000
            self.time_info(result)
        else:
            self.fill(seed, color, delay)

    def border_fill(self) -> None:
        dda(self.image, Dot(0, 0), Dot(0, self.image.height()-1))
        dda(self.image, Dot(0, 0), Dot(self.image.width()-1, 0))
        dda(self.image, Dot(0,self.image.height()-1), \
            Dot(self.image.width()-1, self.image.height()-1))
        dda(self.image, Dot(self.image.width()-1, 0), \
            Dot(self.image.width()-1,self.image.height()-1))

    def cmp_pix(self, pixel: Dot, cmp: QColor) -> bool:
        return self.image.pixelColor(pixel.to_qpoint()) == cmp

    def set_pix(self, pixel: Dot, cmp: QColor) -> None:
        self.image.setPixelColor(pixel.to_qpoint(), cmp)

    def fill(self, seed: Dot, color: QColor, delay: bool):
        stack: list[Dot] = []
        stack.append(seed)
        self.border_fill()
        while stack:
            p_curr = stack.pop()
            self.set_pix(p_curr, color)
            tmp_x = p_curr.x
            p_curr.x += 1
            while not self.cmp_pix(p_curr, Qt.black):
                self.set_pix(p_curr, color)
                p_curr.x += 1
            rx = p_curr.x - 1
            p_curr.x = tmp_x
            p_curr.x -= 1
            while not self.cmp_pix(p_curr, Qt.black):
                self.set_pix(p_curr, color)
                p_curr.x -= 1
            lx = p_curr.x + 1
            p_curr.x = tmp_x
            tmp_y = p_curr.y
            for i in (1, -1):
                p_curr.x = lx
                p_curr.y = tmp_y + i
                while p_curr.x <= rx:
                    flag = False
                    while not self.cmp_pix(
                            p_curr, Qt.black) and not self.cmp_pix(
                                p_curr, color) and p_curr.x <= rx:
                        p_curr.x += 1
                        flag = True
                    if flag:
                        x, y = p_curr.x, p_curr.y
                        if p_curr.x != rx or self.cmp_pix(
                                p_curr, Qt.black) or self.cmp_pix(
                                    p_curr, color):
                            x -= 1
                        stack.append(Dot(x, y))
                    x_input = p_curr.x
                    while (self.cmp_pix(p_curr, Qt.black)
                           or self.cmp_pix(p_curr, color)) and p_curr.x <= rx:
                        p_curr.x += 1
                    if p_curr.x == x_input:
                        p_curr.x += 1
            if delay:
                utils.delay()
                self.image_set()

        self.image_set()

    def time_info(self, time):
        if time is not None:
            text = f'Время закраски: {round(time, 2)} мс'
        else:
            text = f'Время закраски: None'
        QtWidgets.QMessageBox.about(self, "Время", text)

    def add_dot(self, pos: Dot, exactly: bool = False) -> None:
        pos.set_title()

        if exactly and self.figure.data[-1].size():
            last_vertex = self.figure.data[-1].vertices[-1]
            dx, dy = abs(pos.x - last_vertex.x), abs(pos.y - last_vertex.y)
            if dx < dy:
                pos.x = last_vertex.x
            else:
                pos.y = last_vertex.y

        self.figure.add_vertex(pos)

        qp = QPainter(self.image)
        qp.setPen(QPen(Qt.black, 4))
        last_poly = self.figure.data[-1]
        if last_poly.size() > 1:
            dda(self.image, last_poly.vertices[-2], last_poly.vertices[-1])
        qp.end()

        self.image_set()

    def close_poly(self) -> None:
        last_poly = self.figure.data[-1]
        if last_poly.size() < 3:
            return

        qp = QPainter(self.image)
        qp.setPen(QPen(Qt.black, 1))
        self.figure.close_this_polygon()
        dda(self.image, last_poly.vertices[-2], last_poly.vertices[-1])
        qp.end()

        self.image_set()
