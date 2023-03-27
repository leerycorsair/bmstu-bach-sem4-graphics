from PyQt5.QtGui import QImage
import utils
from PyQt5.QtCore import Qt
from data.dot import Dot


def dda(image: QImage, p_begin: Dot, p_end: Dot):
        if p_begin == p_end:
            image.setPixelColor(p_begin.to_qpoint(), Qt.black)
            return

        length = int(max(abs(p_end.x - p_begin.x), abs(p_end.y - p_begin.y)))
        dx = (p_end.x - p_begin.x) / length
        dy = (p_end.y - p_begin.y) / length

        curr_x, curr_y = p_begin.x, p_begin.y
        tmp_x, tmp_y = curr_x, curr_y

        for _ in range(1, length + 2):
            image.setPixelColor(tmp_x, tmp_y, Qt.black)

            curr_x += dx
            curr_y += dy

            rx, ry = utils.round(curr_x), utils.round(curr_y)
            tmp_x, tmp_y = rx, ry