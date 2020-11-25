import sys

from PyQt5 import uic
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QTableWidgetItem


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('main.ui', self)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.con = sqlite3.connect("coffee.sqlite")
        self.cursor = self.con.cursor()
        data = self.cursor.execute("SELECT * FROM Coffee").fetchall()
        self.table.setRowCount(len(data))
        for i in range(len(data)):
            for j in range(1, 7):
                self.table.setItem(i, j - 1, QTableWidgetItem(str(data[i][j])))
        data.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
