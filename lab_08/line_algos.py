from PyQt5.QtGui import QColor, QImage
import tools
from PyQt5.QtCore import Qt
from point import Point


def dda(image: QImage, p_begin: Point, p_end: Point, color: QColor):
    if p_begin == p_end:
        image.setPixelColor(p_begin.x, p_begin.y, color)
        return
    length = int(max(abs(p_end.x - p_begin.x), abs(p_end.y - p_begin.y)))
    if length == 0:
        return
    dx = (p_end.x - p_begin.x) / length
    dy = (p_end.y - p_begin.y) / length
    curr_x, curr_y = p_begin.x, p_begin.y
    tmp_x, tmp_y = curr_x, curr_y
    for _ in range(1, length + 2):
        image.setPixelColor(tmp_x, tmp_y, color)
        curr_x += dx
        curr_y += dy
        rx, ry = tools.round(curr_x), tools.round(curr_y)
        tmp_x, tmp_y = rx, ry
