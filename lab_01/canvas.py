
import tkinter as tk
from config import *


class Canvas(tk.Canvas):
    def __init__(self, master):
        tk.Canvas.__init__(self, master=master)
        self.max_x_delta = CANVAS_DEFAULT_X
        self.max_y_delta = CANVAS_DEFAULT_Y
        self.draw_axes()

    def draw_axes(self):
        self.create_line(0, CANVAS_HEIGHT/2, CANVAS_WIDTH,
                         CANVAS_HEIGHT/2, width=3, arrow="last")
        self.create_text(CANVAS_WIDTH-20, CANVAS_HEIGHT/2+20,
                         text="X", font=('Times New Roman', 14))
        self.create_line(CANVAS_WIDTH/2, CANVAS_HEIGHT,
                         CANVAS_WIDTH/2, 0, width=3, arrow="last")
        self.create_text(CANVAS_WIDTH/2+20, 20, text="Y",
                         font=('Times New Roman', 14))

    def check_circle(self, x, y, r):
        if abs(x - r) > self.max_x_delta:
            self.max_x_delta = abs(x-r)
        if abs(y - r) > self.max_y_delta:
            self.max_y_delta = abs(y-r)
        if abs(x + r) > self.max_x_delta:
            self.max_x_delta = abs(x+r)
        if abs(y + r) > self.max_y_delta:
            self.max_y_delta = abs(y+r)

    def draw_circle(self, x, y, r):
        if self.max_x_delta > self.max_y_delta:
            max_delta = self.max_x_delta
        else:
            max_delta = self.max_y_delta
        tmp_x = x
        tmp_y = y
        x = self.format_x(x)
        y = self.format_y(y)
        r = (r/max_delta)*(CANVAS_WIDTH/2*0.9)
        self.create_oval(x-r, y-r, x+r, y+r, width=2)

    def draw_quad(self, dot1, dot2, dot3, dot4):
        self.create_text(self.format_x(dot1[0]), self.format_y(
            dot1[1])-10, text="({0:.2f};{1:.2f})".format(dot1[0], dot1[1]), fill="blue")
        self.create_text(self.format_x(dot2[0]), self.format_y(
            dot2[1])-10, text="({0:.2f};{1:.2f})".format(dot2[0], dot2[1]), fill="blue")
        self.create_text(self.format_x(dot3[0]), self.format_y(
            dot3[1])-10, text="({0:.2f};{1:.2f})".format(dot3[0], dot3[1]), fill="blue")
        self.create_text(self.format_x(dot4[0]), self.format_y(
            dot4[1])-10, text="({0:.2f};{1:.2f})".format(dot4[0], dot4[1]), fill="blue")

        self.create_line(self.format_x(dot1[0]), self.format_y(
            dot1[1]), self.format_x(dot2[0]), self.format_y(dot2[1]), fill="blue", width=2)
        self.create_line(self.format_x(dot2[0]), self.format_y(
            dot2[1]), self.format_x(dot3[0]), self.format_y(dot3[1]), fill="blue", width=2)
        self.create_line(self.format_x(dot3[0]), self.format_y(
            dot3[1]), self.format_x(dot4[0]), self.format_y(dot4[1]), fill="blue", width=2)
        self.create_line(self.format_x(dot4[0]), self.format_y(
            dot4[1]), self.format_x(dot1[0]), self.format_y(dot1[1]), fill="blue", width=2)

        self.create_oval(self.format_x(dot1[0])-DOT_SIZE, self.format_y(
            dot1[1])-DOT_SIZE, self.format_x(dot1[0])+DOT_SIZE, self.format_y(
            dot1[1])+DOT_SIZE, fill="blue")
        self.create_oval(self.format_x(dot2[0])-DOT_SIZE, self.format_y(
            dot2[1])-DOT_SIZE, self.format_x(dot2[0])+DOT_SIZE, self.format_y(
            dot2[1])+DOT_SIZE, fill="blue")
        self.create_oval(self.format_x(dot3[0])-DOT_SIZE, self.format_y(
            dot3[1])-DOT_SIZE, self.format_x(dot3[0])+DOT_SIZE, self.format_y(
            dot3[1])+DOT_SIZE, fill="blue")
        self.create_oval(self.format_x(dot4[0])-DOT_SIZE, self.format_y(
            dot4[1])-DOT_SIZE, self.format_x(dot4[0])+DOT_SIZE, self.format_y(
            dot4[1])+DOT_SIZE, fill="blue")

    def format_x(self, x):
        if self.max_x_delta > self.max_y_delta:
            max_delta = self.max_x_delta
        else:
            max_delta = self.max_y_delta
        x = (x/max_delta)*(CANVAS_WIDTH/2*0.9)
        x = x + CANVAS_WIDTH/2
        return x

    def format_y(self, y):
        if self.max_x_delta > self.max_y_delta:
            max_delta = self.max_x_delta
        else:
            max_delta = self.max_y_delta
        y = (y/max_delta) * (CANVAS_HEIGHT/2*0.9)
        y = - (y - CANVAS_HEIGHT/2)
        return y

    def clear(self):
        self.delete("all")

    def draw_dots(self, dots_matrix):
        self.clear()
        self.draw_axes()
        for dots_list in dots_matrix:
            for dot in dots_list:
                if abs(dot[0]) > self.max_x_delta:
                    self.max_x_delta = abs(dot[0])
                if abs(dot[1]) > self.max_y_delta:
                    self.max_y_delta = abs(dot[1])
        color_list = ["#FF0000", "#00FF00"]

        for i in range(len(dots_matrix)):
            for j in range(len(dots_matrix[i])):
                new_x = self.format_x(dots_matrix[i][j][0])
                new_y = self.format_y(dots_matrix[i][j][1])
                self.create_oval(new_x-DOT_SIZE, new_y-DOT_SIZE,
                                 new_x+DOT_SIZE, new_y+DOT_SIZE, fill=color_list[i])
                self.create_text(new_x, new_y - 10, text="D["+str(j+1)+"]("+str(
                    dots_matrix[i][j][0])+";"+str(dots_matrix[i][j][1])+")", fill=color_list[i])
