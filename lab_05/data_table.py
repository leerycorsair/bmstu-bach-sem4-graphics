from PyQt5 import QtWidgets


class DataTable(QtWidgets.QTableWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)

    def add_dot(self, dot) -> None:
        curr_row = self.rowCount()
        self.insertRow(curr_row)

        self.setItem(curr_row, 0, QtWidgets.QTableWidgetItem(dot.title))
        self.setItem(curr_row, 1, QtWidgets.QTableWidgetItem(str(dot.x)))
        self.setItem(curr_row, 2, QtWidgets.QTableWidgetItem(str(dot.y)))

    def clear(self) -> None:
        self.setRowCount(0)