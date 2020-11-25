import sys

from PyQt5 import uic
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QTableWidgetItem, QWidget


class EditWindow(QWidget):
    def __init__(self, parent, index):
        super().__init__()
        self.initUI(parent, index)

    def initUI(self, parent, index):
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.parent = parent
        self.index = index
        self.button_Done.clicked.connect(self.apply)

    def apply(self):
        self.parent.apply(self.index, self.sortName.text(), self.roast.text(), self.type.currentText(),
                          self.description.toPlainText(), str(self.price.value()), str(self.size.value()))

    def closeEvent(self, event):
        self.parent.editWindow = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('main.ui', self)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.con = sqlite3.connect("coffee.sqlite")
        self.cursor = self.con.cursor()
        self.updateTable()
        self.button_Edit.clicked.connect(self.openWindow)
        self.button_Add.clicked.connect(self.openWindow)
        self.editWindow = None

    def openWindow(self):
        if self.editWindow is not None:
            return
        if self.sender() is self.button_Edit:
            self.editWindow = EditWindow(self, self.table.currentRow() + 1)
        else:
            self.editWindow = EditWindow(self, self.table.rowCount() + 1)
        self.editWindow.show()
        if self.sender() is self.button_Edit:
            self.editWindow.sortName.setText(self.table.item(self.table.currentRow(), 0).text())
            self.editWindow.roast.setText(self.table.item(self.table.currentRow(), 1).text())
            if self.table.item(self.table.currentRow(), 2).text() == "Молотый":
                self.editWindow.type.setCurrentIndex(0)
            else:
                self.editWindow.type.setCurrentIndex(1)
            self.editWindow.description.setPlainText(self.table.item(self.table.currentRow(), 3).text())
            self.editWindow.price.setValue(int(self.table.item(self.table.currentRow(), 4).text()))
            self.editWindow.size.setValue(int(self.table.item(self.table.currentRow(), 5).text()))

    def apply(self, index, sort, roast, type, description, price, size):
        if index > self.table.rowCount():
            self.cursor.execute("INSERT INTO Coffee VALUES(?, ?, ?, ?, ?, ?, ?)",
                                [index, sort, roast, type, description, price, size])
        else:
            self.cursor.execute("UPDATE Coffee SET Sort = '{}', roastDegree = '{}', type = '{}', description = '{}',"
                                " price = {}, size = {} where ID = {}".format(sort, roast, type,
                                                                              description, price, size, index))
        self.con.commit()
        self.editWindow.close()
        self.updateTable()

    def updateTable(self):
        self.table.setRowCount(0)
        data = self.cursor.execute("SELECT * FROM Coffee").fetchall()
        self.table.setRowCount(len(data))
        for i in range(len(data)):
            for j in range(1, 7):
                self.table.setItem(i, j - 1, QTableWidgetItem(str(data[i][j])))
        data.clear()

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
