import os
import csv
import sys
import shutil
import webbrowser
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QGridLayout,QTableWidgetItem
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import win32gui


path = "./db/db_gammes.csv"
path2 = "./db/db_gammes2.csv"

class test(object):
    def __init__(self):
        pass
   
    def leftClick(self, row, column):
        print('left',row,column)
   
   
    def rightClick(self, row, column):
        print('right',row,column)

class App(QWidget): 

    def __init__(self):
        super().__init__()
        self.colwidth = 296
        self.left = 550
        self.top = 100
        self.width = 686
        self.height = 824
        # self.rownums = 1932
        # self.colnums = 2
        self.initUI()
        
        self.test = test()
        
           
    def initUI(self):
        
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.createTable()
        self.layout = QGridLayout()
        self.layout.addWidget(self.tableWidget,0,0)
        self.setLayout(self.layout) 
        self.setObjectName("Gammes")
        # Show widget
        self.show()

    def createTable(self):

       # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setEditTriggers(QtWidgets.QTreeView.NoEditTriggers) 

        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setVisible(True)

        origin = r"./db/db_gammes.csv"
        copy = r"./db/db_gammes2.csv"
        if os.path.isfile(path2):
            os.remove(path2)

        shutil.copyfile(origin, copy)
        with open(path, newline='') as csv_file:
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(2)
            my_file = csv.reader(csv_file, delimiter=',', quotechar='|')
            for row_data in my_file:
                row = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row)
                if len(row_data) > 10:
                    self.tableWidget.setColumnCount(len(row_data))
                for column, stuff in enumerate(row_data):
                    item = QTableWidgetItem(stuff)
                    self.tableWidget.setItem(row, column, item)
            for i in range(1931):
                self.tableWidget.setColumnWidth(i, self.colwidth)
            
        fnt = self.tableWidget.font()
        fnt.setFamily("Segoe UI")
        fnt.setPointSize(14)
        fnt.setBold(True)
        self.tableWidget.setFont(fnt)
                

        self.tableWidget.move(0,30)
        self.tableWidget.viewport().installEventFilter(self)
        
    def eventFilter(self, source, event):
        if self.tableWidget.selectedIndexes() != []:
            
            if event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    row = self.tableWidget.currentRow()
                    col = self.tableWidget.currentColumn()
                    self.tableWidget.setItem(row, col, QTableWidgetItem('VALIDE'))
                    #self.test.leftClick(row, col)

                    with open(path2, 'w') as csv_file:
                        writer = csv.writer(csv_file, dialect='excel')
                        for row in range(self.tableWidget.rowCount()):
                            rowdata = []
                            for column in range(self.tableWidget.columnCount()):
                                item = self.tableWidget.item(row, column)
                                rowdata.append(str(item.text()))
                                # if item is not None:
                                #     rowdata.append(str(item.text()).encode('utf8'))
                                # else:
                                #     rowdata.append('')
                            writer.writerow(rowdata)
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                self.close()



        return QtCore.QObject.event(source, event)

        
    
# if __name__ == '__main__':

#     app = QApplication(sys.argv)
#     ex = App()
#     sys.exit(app.exec_())