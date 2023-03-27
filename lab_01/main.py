import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox


from config import *
import datasheet
import canvas
import geometry_sollution


class Program(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Geometry Solver")
        self.geometry(APP_SIZE + "+" + "10+10")
        self.resizable(width=0, height=0)
        self.configure(background=BRIGHT_GREEN)
        self.create_widgets()

    def create_widgets(self):

        self.right_frame = tk.LabelFrame(
            self, padx=15, pady=15, text="Графическое представление",foreground=WHITE, font=DEFAULT_FONT, background=BRIGHT_GREEN)
        self.right_frame.grid(row=0, column=1)

        self.canvas = canvas.Canvas(master=self.right_frame,)
        self.canvas.configure(
            bg="white", width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self.canvas.grid(row=1, column=0)

        self.left_frame = tk.Frame(self, padx=15, pady=15, background=BRIGHT_GREEN)
        self.left_frame.grid(row=0, column=0)

        self.var_1 = datasheet.DataSheet(master=self.left_frame,
                                         canvas=self.canvas, id=0)
        self.var_1.configure(text='Множество 1', font=DEFAULT_FONT, foreground=WHITE)
        self.var_1.grid(row=0, column=0, padx=10)

        self.var_2 = datasheet.DataSheet(master=self.left_frame,
                                         canvas=self.canvas, id=1)
        self.var_2.configure(text='Множество 2', font=DEFAULT_FONT, foreground=WHITE)
        self.var_2.grid(row=1, column=0, padx=10)

        self.run_button = tk.Button(
            self.left_frame, width=15, background=DARK_GREEN,foreground=WHITE,  text="Найти решение", font=DEFAULT_FONT, command=self.find_sollution)
        self.run_button.grid(row=2, column=0, pady = 10)

        self.info_frame = tk.Frame(self.left_frame, background= BRIGHT_GREEN, padx =0, pady=0)
        self.info_frame.grid(row=3, column = 0)
        self.prog_info_button = tk.Button(
            self.info_frame, width=15,background=DARK_GREEN,foreground=WHITE, text="О программе", font=DEFAULT_FONT, command=self.show_prog_info)
        self.prog_info_button.grid(row=0, column=0, pady=0, padx= 5)

        self.auth_info_button = tk.Button(
            self.info_frame, width=15,background=DARK_GREEN,foreground=WHITE, text="Об авторе", font=DEFAULT_FONT, command=self.show_auth_info)
        self.auth_info_button.grid(row=0, column=1, pady=0, padx= 5)

    def show_prog_info(self):
        info = '''Данная программа предназначенна для решения следующей задачи:
На плоскости заданы два множества точек. Найти пару окружностей, каждая из \
которых проходит хотя бы через три различные точки одного и того же множества \
(точки берутся из разных множеств для различных окружностей), для которых \
площадь четырехугольника, образованного центрами окружностей и точками касания \
общей внешней касательной, максимальная.

Программа выполнена в рамках учебного курса: Компьютерная графика.
Руководитель курса: Куров А.В.

Версия: 1.0.0'''
        messagebox.showinfo(title="О программе", message=info)

    def show_auth_info(self):
        info = "Автором данной программы является\nстудент МГТУ им. Н.Э. Баумана группы ИУ7-46Б,\n\
Леонов Владислав Вячеславович"
        messagebox.showinfo(title="Об авторе", message=info)

    def find_sollution(self):
        answer = geometry_sollution.solve(
            self.var_1.dots[self.var_1.id], self.var_2.dots[self.var_2.id])
        if answer.status_code == 0:
            self.canvas.check_circle(
                answer.first_circle[0], answer.first_circle[1], answer.first_circle[2])
            self.canvas.check_circle(
                answer.second_circle[0], answer.second_circle[1], answer.second_circle[2])
            self.canvas.draw_dots(self.var_1.dots)
            self.canvas.draw_circle(*answer.first_circle)
            self.canvas.draw_circle(*answer.second_circle)
            self.canvas.draw_quad(
                answer.quadrilateral[0], answer.quadrilateral[1], answer.quadrilateral[2], answer.quadrilateral[3])
        messagebox.showinfo(message=answer.create_message(), title="Ответ")


def main():
    application = Program()
    application.mainloop()


if(__name__ == "__main__"):
    main()
