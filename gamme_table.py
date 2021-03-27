import sys
import os
import csv
from PyQt5.QtWidgets import QTableWidget, QApplication, QMainWindow, QTableWidgetItem, QFileDialog


class MyTable(QTableWidget):
    def __init__(self, r, c):
        super().__init__(r, c)
        self.check_change = True
        self.init_ui()

    def init_ui(self):
        self.cellChanged.connect(self.c_current)
        self.show()

    def c_current(self):
        colonne = 0
        if self.check_change:
            colonne = self.currentColumn()
        return colonne



    def open_sheet(self):
        self.check_change = False
        path = "./db/db_gammes.csv"
        with open(path, newline='') as csv_file:
            self.setRowCount(0)
            self.setColumnCount(2)
            my_file = csv.reader(csv_file, delimiter=',', quotechar='|')
            for row_data in my_file:
                row = self.rowCount()
                self.insertRow(row)
                if len(row_data) > 10:
                    self.setColumnCount(len(row_data))
                for column, stuff in enumerate(row_data):
                    item = QTableWidgetItem(stuff)
                    self.setItem(row, column, item)
        self.check_change = True


class Sheet(QMainWindow):
    def __init__(self):
        super().__init__()
        colonne = 0
        self.form_widget = MyTable(10, 10)
        self.setCentralWidget(self.form_widget)
        col_headers = ['Ref', 'Gamme']
        self.form_widget.setHorizontalHeaderLabels(col_headers)

        self.form_widget.open_sheet()
        colonne = self.form_widget.c_current()
        print(colonne)

        self.show()

app = QApplication(sys.argv)
sheet = Sheet()
sys.exit(app.exec_())