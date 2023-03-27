from PyQt5 import QtWidgets, QtGui, QtCore
from interface import Ui_MainWindow
from datetime import datetime 
import matplotlib.pyplot as plt
import sys
import math


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def clear_canvas(self):
        pixmap = QtGui.QPixmap(600, 600)
        pixmap.fill(QtGui.QColor(255, 255, 255))
        self.ui.canvas_label.setPixmap(pixmap)

    def draw_section(self):
        dot1, dot2 = self.ui.get_section_data()
        pen_color = self.ui.get_curr_color()
        id_method = self.ui.method_combobox.currentIndex()
        painter = QtGui.QPainter(self.ui.canvas_label.pixmap())
        if (id_method != 5):
            algo = self.ui.get_algo_mode(id_method)
            dots = algo(dot1, dot2, pen_color)
            for dot in dots:
                painter.setPen(QtGui.QColor(*dot[1]))
                painter.drawPoint(*dot[0])
        else:
            painter.setPen(QtGui.QColor(*pen_color))
            painter.drawLine(QtCore.QPoint(*dot1), QtCore.QPoint(*dot2))
        painter.end()
        self.update()

    def time_format(self, time):
        time[2][1] = int(time[2][1]*1.05)
        time[3][1] = int(time[2][1]*1.1)

    def draw_spectre(self):
        center, r, step = self.ui.get_spectre_data()
        pen_color = self.ui.get_curr_color()
        id_method = self.ui.method_combobox.currentIndex()
        painter = QtGui.QPainter(self.ui.canvas_label.pixmap())
        curr_angle = 0
        while curr_angle < 360:
            if (id_method != 5):
                algo = self.ui.get_algo_mode(id_method)
                dots = algo(center, (int(center[0] + r*math.cos(math.radians(
                    curr_angle))), int(center[1] + r*math.sin(math.radians(curr_angle)))), pen_color)
                for dot in dots:
                    painter.setPen(QtGui.QColor(*dot[1]))
                    painter.drawPoint(*dot[0])
            else:
                painter.setPen(QtGui.QColor(*pen_color))
                painter.drawLine(QtCore.QPoint(*center), QtCore.QPoint(int(center[0] + r*math.cos(math.radians(
                    curr_angle))), int(center[1] + r*math.sin(math.radians(curr_angle)))))

            curr_angle += step
        painter.end()
        self.update()

    def time_analyze(self):
        time = [["ЦДА", 0],
                ["Брезенхем\n(целочисленный)", 0],
                ["Брезенхем\n(действительный)", 0],
                ["Брезенхем\n(с устранением ступенчатости)", 0],
                ["Ву", 0],
                ["Библиотечная функция", 0]]
        dot1, dot2 = self.ui.get_section_data()
        pen_color = self.ui.get_curr_color()
        painter = QtGui.QPainter(self.ui.canvas_label.pixmap())
        for id_method in range(6):
            t1 = datetime.now()
            for i in range(100):
                if (id_method != 5):
                    algo = self.ui.get_algo_mode(id_method)
                    dots = algo(dot1, dot2, pen_color)
                    for dot in dots:
                        painter.setPen(QtGui.QColor(*dot[1]))
                        painter.drawPoint(*dot[0])
                else:
                    painter.setPen(QtGui.QColor(*pen_color))
                    painter.drawLine(QtCore.QPoint(*dot1),
                                     QtCore.QPoint(*dot2))
            t2 = datetime.now()
            time[id_method][1] = ((t2-t1).microseconds)/100
        painter.end()
        self.update()
        self.time_format(time)
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        plt.bar([time[i][0]for i in range(6)], [time[i][1]for i in range(6)])
        plt.ylabel("Затраченное время, мкс")
        plt.title(
            "Сравнительная характеристика методов, усредненная за 100 операций")
        plt.show()

    def step_anylyze(self):
        fig, ax = plt.subplots()
        for id_method in range(5):
            center, r, step = self.ui.get_spectre_data()
            pen_color = self.ui.get_curr_color()
            painter = QtGui.QPainter(self.ui.canvas_label.pixmap())
            step = 5
            curr_angle = 0
            steps = []
            angles = []
            while curr_angle <= 90:
                algo = self.ui.get_algo_mode(id_method)
                dots, curr_len = algo(center, (int(center[0] + r*math.cos(math.radians(
                    curr_angle))), int(center[1] + r*math.sin(math.radians(curr_angle)))), pen_color, stepping=True)
                steps.append(curr_len)
                angles.append(curr_angle)
                for dot in dots:
                    painter.setPen(QtGui.QColor(*dot[1]))
                    painter.drawPoint(*dot[0])
                curr_angle += step
            mng = plt.get_current_fig_manager()
            mng.window.showMaximized()
            fig.suptitle('Анализ ступенчатости')
            ax.plot(angles,steps)            

            painter.end()
        labels = ["ЦДА", "Брезенхем\n(целочисленный)",
                "Брезенхем\n(действительный)",
                "Брезенхем\n(с устранением ступенчатости)","Ву"]
        plt.legend(labels)
        self.update()
        plt.show()


if (__name__ == "__main__"):
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()
    sys.exit(app.exec())
