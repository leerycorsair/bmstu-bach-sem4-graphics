import tkinter as tk
from tkinter import messagebox
from config import *


class DotEntry(tk.Tk):
    def __init__(self, datasheet, mode):
        tk.Tk.__init__(self)
        self.title("Ввод точки")
        self.attributes("-topmost", True)
        self.resizable(0, 0)
        self.configure(background=BRIGHT_GREEN)
        self.datasheet = datasheet
        self.mode = mode
        self.create_entries()
        self.mainloop()

    def create_entries(self):
        self.x_label = tk.LabelFrame(
            self, text="X", font=DEFAULT_FONT, background=BRIGHT_GREEN, foreground=WHITE)
        self.x_label.grid(row=0, column=0, padx=10, pady=10)
        self.x_entry = tk.Entry(self.x_label, width=20,
                                font=DEFAULT_FONT)
        self.x_entry.grid(row=0, column=0)

        self.y_label = tk.LabelFrame(
            self, text="Y", font=DEFAULT_FONT, background=BRIGHT_GREEN, foreground=WHITE)
        self.y_label.grid(row=1, column=0, padx=10, pady=10)
        self.y_entry = tk.Entry(self.y_label, width=20,
                                font=DEFAULT_FONT)
        self.y_entry.grid(row=0, column=0)

        if (self.mode == "add"):
            self.confirm_button = tk.Button(
                self, text="Oк", font=DEFAULT_FONT, background=DARK_GREEN, foreground=WHITE, width=20, command=self.add_dot)
            self.confirm_button.grid(row=2, column=0, pady=10)
        else:
            self.i_label = tk.LabelFrame(
                self, text="Номер точки", font=DEFAULT_FONT, background=BRIGHT_GREEN, foreground=WHITE)
            self.i_label.grid(row=2, column=0)
            self.i_entry = tk.Entry(self.i_label, width=20,
                                    font=DEFAULT_FONT)
            self.i_entry.grid(row=0, column=0)
            self.confirm_button = tk.Button(
                self, text="Oк", font=DEFAULT_FONT, width=20, command=self.edit_dot, background=DARK_GREEN, foreground=WHITE)
            self.confirm_button.grid(row=3, column=0, pady=10)

    def add_dot(self):
        try:
            x_coord = float(self.x_entry.get())
            y_coord = float(self.y_entry.get())
            self.datasheet.add_dot(x=x_coord, y=y_coord)
            self.destroy()
        except:
            messagebox.showerror(
                title="Ошибка", message="Координаты точки должны быть действительными числами. Повторите ввод.")

    def edit_dot(self):
        try:
            x_coord = float(self.x_entry.get())
            y_coord = float(self.y_entry.get())
            item = int(self.i_entry.get())
            if (item <= 0):
                raise Exception()
            self.datasheet.edit_dot(x=x_coord, y=y_coord, i=item - 1)
            self.destroy()
        except:
            messagebox.showerror(
                title="Ошибка", message="Координаты точки должны быть действительными числами. Номер - целое положительное. Повторите ввод.")
