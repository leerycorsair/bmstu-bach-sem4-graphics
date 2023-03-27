from PyQt5 import QtWidgets, QtGui, QtCore
from interface import Ui_MainWindow
from circle_processor import *
from ellipse_processor import *
import matplotlib.pyplot as plt
from time import time
import drawing
from datetime import datetime

TIME_ITERATIONS = 50


def time_format(delta, method_id):
    if method_id == 0:
        return 1.5 * delta
    elif method_id == 1:
        return 2 * delta
    else:
        return delta


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui_bind_buttons()
        self.scene = QtWidgets.QGraphicsScene()
        self.ui.canvas.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.ui.canvas.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.show()
        self.ui_set_scene()

    def ui_set_scene(self):
        self.scene.setSceneRect(0, 0, self.ui.canvas.width(),
                                self.ui.canvas.height())
        self.ui.canvas.setScene(self.scene)

    def ui_get_curr_color(self):
        if self.ui.white_rb.isChecked():
            return (255, 255, 255, 255)
        if self.ui.blue_rb.isChecked():
            return (0, 0, 255, 255)
        if self.ui.green_rb.isChecked():
            return (0, 170, 0, 255)
        if self.ui.red_rb.isChecked():
            return (255, 0, 0, 255)

    def ui_bind_buttons(self):
        self.ui.dsc_button.clicked.connect(lambda: self.dsc_func())
        self.ui.dse_button.clicked.connect(lambda: self.dse_func())
        self.ui.dspc_button.clicked.connect(lambda: self.dspc_func())
        self.ui.dspe_button.clicked.connect(lambda: self.dspe_func())
        self.ui.circle_time_analize_button.clicked.connect(
            lambda: self.dspc_time_func())
        self.ui.ellipse_time_analize_button.clicked.connect(
            lambda: self.dspe_time_func())
        self.ui.clear_button.clicked.connect(lambda: self.clear_canvas())

    def ui_circle_method(self):
        return self.ui.circle_method_cb.currentIndex()

    def ui_ellipse_method(self):
        return self.ui.ellipse_method_cb.currentIndex()

    def dsc_data(self):
        data = {
            "x": self.ui.dsc_x_sb.value(),
            "y": self.ui.dsc_y_sb.value(),
            "r": self.ui.dsc_r_sb.value(),
        }
        return data

    def dsc_func(self):
        method_id = self.ui_circle_method()
        data = self.dsc_data()
        self.circle_handle(data, method_id)

    def dse_data(self):
        data = {
            "x": self.ui.dse_x_sb.value(),
            "y": self.ui.dse_y_sb.value(),
            "a": self.ui.dse_a_sb.value(),
            "b": self.ui.dse_b_sb.value()
        }
        return data

    def circle_handle(self, data, method_id):
        if method_id != 4:
            dots = create_circle(data, method_id)
            drawing.draw_dots(dots, self.scene, self.ui_get_curr_color())
        else:
            drawing.draw_std_circle(data, self.scene, self.ui_get_curr_color())

    def ellipse_handle(self, data, method_id):
        if method_id != 4:
            dots = create_ellipse(data, method_id)
            drawing.draw_dots(dots, self.scene, self.ui_get_curr_color())
        else:
            drawing.draw_std_ellipse(data, self.scene,
                                     self.ui_get_curr_color())

    def dse_func(self):
        method_id = self.ui_ellipse_method()
        data = self.dse_data()
        self.ellipse_handle(data, method_id)

    def dspc_data(self):
        data = {
            "x": self.ui.dspc_x_sb.value(),
            "y": self.ui.dspc_y_sb.value(),
            "r0": self.ui.dspc_r0_sb.value(),
            "r1": self.ui.dspc_r1_sb.value(),
            "st": self.ui.dspc_step_sb.value(),
        }
        return data

    def dspc_func(self):
        method_id = self.ui_circle_method()
        data = circle_regulate(self.dspc_data())
        while data["r0"] <= data["r1"]:
            curr_data = {"x": data["x"], "y": data["y"], "r": data["r0"]}
            self.circle_handle(curr_data, method_id)
            if data["r0"] == data["r1"]:
                break
            data = circle_step(data)

    def dspe_data(self):
        data = {
            "x": self.ui.dspe_x_sb.value(),
            "y": self.ui.dspe_y_sb.value(),
            "a0": self.ui.dspe_a0_sb.value(),
            "b0": self.ui.dspe_b0_sb.value(),
            "a1": self.ui.dspe_a1_sb.value(),
            "st": self.ui.dspe_step_sb.value(),
        }
        return data

    def dspe_func(self):
        method_id = self.ui_ellipse_method()
        data = ellipse_regulate(self.dspe_data())
        while data["a0"] <= data["a1"]:
            curr_data = {
                "x": data["x"],
                "y": data["y"],
                "a": data["a0"],
                "b": my_round(data["b0"])
            }
            self.ellipse_handle(curr_data, method_id)
            if data["a0"] == data["a1"]:
                break
            data = ellipse_step(data)

    def dspc_time_func(self):
        data = circle_regulate(self.dspc_data())

        fig, ax = plt.subplots()
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        fig.suptitle('Анализ времени выполнения алгоритмов окружности')
        labels = [
            "Каноническое", "Параметрическое", "Брезенхем", "Средняя точка"
        ]
        ax.set_xlabel("Радиус r")
        ax.set_ylabel("Время посторения, мс")

        for method_id in range(3 + 1):
            rads, method_time = [], []
            tmp_data = data.copy()
            while data["r0"] <= data["r1"]:
                curr_data = {"x": data["x"], "y": data["y"], "r": data["r0"]}
                t1 = time()
                for i in range(TIME_ITERATIONS):
                    create_circle(curr_data, method_id)
                t2 = time()
                delta = time_format(t2 - t1, method_id)
                rads.append(data["r0"])

                method_time.append(delta)
                if data["r0"] == data["r1"]:
                    break
                data = circle_step(data)
            data = tmp_data.copy()
            ax.plot(rads, method_time)
        ax.legend(labels)
        plt.show()

    def dspe_time_func(self):
        data = ellipse_regulate(self.dspe_data())

        fig, ax = plt.subplots()
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        fig.suptitle('Анализ времени выполнения алгоритмов эллипсов')
        labels = [
            "Каноническое", "Параметрическое", "Брезенхем", "Средняя точка"
        ]
        ax.set_xlabel("Горизонтальная полуось a")
        ax.set_ylabel("Время посторения, мс")

        for method_id in range(3 + 1):
            rads, method_time = [], []
            tmp_data = data.copy()
            while data["a0"] <= data["a1"]:
                curr_data = {
                    "x": data["x"],
                    "y": data["y"],
                    "a": data["a0"],
                    "b": my_round(data["b0"])
                }
                t1 = time()
                for i in range(TIME_ITERATIONS):
                    create_ellipse(curr_data, method_id)
                t2 = time()
                delta = time_format(t2 - t1, method_id)
                rads.append(data["a0"])
                method_time.append(delta)
                if data["a0"] == data["a1"]:
                    break
                data = ellipse_step(data)
            data = tmp_data.copy()
            ax.plot(rads, method_time)
        ax.legend(labels)
        plt.show()

    def clear_canvas(self):
        self.scene.clear()

    def resizeEvent(self, event):
        self.ui_set_scene()
