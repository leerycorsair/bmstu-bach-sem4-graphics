import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import random

import dotentry
from config import *


class DataSheet(tk.LabelFrame):
    dots = []
    dots.append([])
    dots.append([])

    def __init__(self, master, canvas, id):
        tk.LabelFrame.__init__(self, master=master)
        self.canvas = canvas
        self.configure(background=BRIGHT_GREEN)
        self.id = id
        self.create()

    def create(self):

        self.style = ttk.Style()
        self.style.configure("mystyle.Treeview", font=DEFAULT_FONT)
        self.style.configure("mystyle.Treeview.Heading",font=DEFAULT_FONT)

        self.table_frame = tk.Frame(self, padx=15, background=BRIGHT_GREEN)
        self.table_frame.grid(row=0, column=0)
        self.table = ttk.Treeview(self.table_frame, style= "mystyle.Treeview")
        self.table.configure(columns=['Координата X', 'Координата Y'])
        self.table.heading('#0', text='N')
        self.table.heading('Координата X', text='Координата X')
        self.table.heading('Координата Y', text='Координата Y')
        self.table.column('Координата X', width=185, anchor='center')
        self.table.column('Координата Y', width=185, anchor='center')
        self.table.column('#0', width=50, anchor='center')
        self.table.grid(row=0, column=0)

        self.buttons_frame = tk.Frame(self, padx=15, background=BRIGHT_GREEN)
        self.buttons_frame.grid(row=1, column=0)

        self.add_random = tk.Button(
            self.buttons_frame, width=5, text="🎲", background=DARK_GREEN, foreground=WHITE, font=BIG_FONT, command=self.add_random_dot)
        self.add_random.grid(row=0, column=0, pady=10, padx=10)

        self.add_dot_button = tk.Button(
            self.buttons_frame, width=5, text="+", background=DARK_GREEN, foreground=WHITE, font=BIG_FONT, command=self.create_add_entry)
        self.add_dot_button.grid(row=0, column=1, pady=10, padx=10)

        self.del_dot_button = tk.Button(
            self.buttons_frame, width=5, text="-", background=DARK_GREEN, foreground=WHITE, font=BIG_FONT, command=self.del_dot)
        self.del_dot_button.grid(row=0, column=2, pady=10, padx=10)

        self.edit_dot_button = tk.Button(
            self.buttons_frame, width=5, height=1, text="✎", background=DARK_GREEN, foreground=WHITE, font=BIG_FONT, command=self.create_edit_entry)
        self.edit_dot_button.grid(row=0, column=3, pady=10, padx=10)

        self.wipe_dot_button = tk.Button(
            self.buttons_frame, width=5, text="🚮", background=DARK_GREEN, foreground=WHITE, font=BIG_FONT, command=self.wipe_dots)
        self.wipe_dot_button.grid(row=0, column=4, pady=10, padx=10)

    def update_table(self):
        self.table.delete(*self.table.get_children())
        for i in range(len(self.dots[self.id])):
            self.table.insert("", "end", text=i+1,
                              values=self.dots[self.id][i])

    def add_random_dot(self):
        x = random.randint(round(-self.canvas.max_x_delta),
                           round(self.canvas.max_x_delta))
        y = random.randint(round(-self.canvas.max_y_delta),
                           round(self.canvas.max_y_delta))
        if ((x, y) not in self.dots[self.id]):
            self.dots[self.id].append((x, y))
            self.canvas.draw_dots(self.dots)
            self.update_table()
        else:
            self.add_random_dot()

    def create_add_entry(self):
        self.dot_entry = dotentry.DotEntry(datasheet=self, mode="add")

    def add_dot(self, x, y):
        if ((x, y) not in self.dots[self.id]):
            self.dots[self.id].append((x, y))
            self.canvas.draw_dots(self.dots)
            self.update_table()
        else:
            messagebox.showinfo(
                title="Ошибка", message="Данная точка уже присутствует в данном множестве.")

    def del_dot(self):
        selected_items = self.table.selection()
        for selected_item in selected_items:
            item = tuple([float(x)
                          for x in self.table.item(selected_item)["values"]])
            self.dots[self.id].remove(item)
            self.canvas.max_x_delta = CANVAS_DEFAULT_X
            self.canvas.max_y_delta = CANVAS_DEFAULT_Y
            self.canvas.draw_dots(self.dots)
        self.update_table()

    def wipe_dots(self):
        selected_items = self.table.get_children()
        for selected_item in selected_items:
            item = tuple([float(x)
                          for x in self.table.item(selected_item)["values"]])
            self.dots[self.id].remove(item)
            self.canvas.max_x_delta = CANVAS_DEFAULT_X
            self.canvas.max_y_delta = CANVAS_DEFAULT_Y
            self.canvas.draw_dots(self.dots)
        self.update_table()

    def create_edit_entry(self):
        self.dot_entry = dotentry.DotEntry(datasheet=self, mode="edit")

    def edit_dot(self, x, y, i):
        if (i+1 <= len(self.dots[self.id])):
            self.dots[self.id][i] = (x, y)
            self.canvas.max_x_delta = CANVAS_DEFAULT_X
            self.canvas.max_y_delta = CANVAS_DEFAULT_Y
            self.canvas.draw_dots(self.dots)
            self.update_table()
        else:
            messagebox.showerror(
                title="Ошибка", message="Введенная вами точка отсутствует в таблице")
