from PyQt5 import QtWidgets, QtGui
import my_round

class Dot():
    def __init__(self, x, y):
        self.x = x
        self.y = y


def draw_dots(dots: list[Dot], scene: QtWidgets.QGraphicsScene, color: tuple):
    for dot in dots:
        draw_dot(dot, scene, color)


def draw_dot(dot: Dot, scene: QtWidgets.QGraphicsScene, color: tuple):
    scene.addLine(dot.x, dot.y, dot.x, dot.y, QtGui.QPen(QtGui.QColor(*color)))


def draw_std_circle(data: dict, scene: QtWidgets.QGraphicsScene,
                    color: tuple) -> None:
    scene.addEllipse(data["x"] - data["r"], data["y"] - data["r"],
                     2 * data["r"], 2 * data["r"],
                     QtGui.QPen(QtGui.QColor(*color)))


def draw_std_ellipse(data: dict, scene: QtWidgets.QGraphicsScene,
                     color: tuple) -> None:
    scene.addEllipse(data["x"] - data["a"], data["y"] - data["b"],
                     2 * data["a"], 2 * data["b"],
                     QtGui.QPen(QtGui.QColor(*color)))
