import os
from PyQt5 import QtCore, QtWidgets, QtGui
from datetime import datetime, date
from paying_widget import Ui_Form
from csv_manip import *
from printer_testing import printing
from table_testing import App
from openpyxl import Workbook, load_workbook

db_cl_file = "./db/db_clients.csv"
db_gm_file = "./db/db_gamme.xlsx"
db_gm_csv = "./db/db_gammes2.csv"


class MyTable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = App()
        self.ui.show()
        #self.ui.closeEvent(self, QtCore.QEvent.MouseButtonRelease)

class MyWidget(QtWidgets.QWidget):
    num = 0
    row = 0
    op = 0
    outsider = 0
    ind = 1
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)


        self.ui.lineEdit_1.setValidator(QtGui.QDoubleValidator(0.999, 99.999, 3))
        #self.ui.lineEdit_2.setValidator(QtGui.QDoubleValidator(0.999, 99.999, 3))
        self.ui.lineEdit_3.setValidator(QtGui.QDoubleValidator(0.999, 99.999, 3))
        self.ui.lineEdit_5.setValidator(QtGui.QDoubleValidator(0.999, 99.999, 3))
        self.ui.lineEdit_7.setValidator(QtGui.QDoubleValidator(0.999, 99.999, 3))

        self.ui.lineEdit_4.returnPressed.connect(self.calc_montant)
        self.ui.lineEdit_6.returnPressed.connect(self.calc_remise)
        self.ui.lineEdit_8.returnPressed.connect(self.calc_credit)
        self.ui.CB1.installEventFilter(self)
        self.ui.CB2.installEventFilter(self)
        self.ui.CB3.installEventFilter(self)
        self.ui.pb2.clicked.connect(self.reload)
        self.ui.pb1.clicked.connect(self.reload2)
        if self.outsider == 0:
            self.ui.lineEdit_6.setText("")
        else:
            self.ui.lineEdit_6.setText(str(self.outsider))



    def calc_montant(self):
        
        qty = self.ui.lineEdit_1
        p_uni = self.ui.lineEdit_3
 
        qty1 = str(qty.text())
        p_uni1 = str(p_uni.text())

        if qty1 != "" or p_uni1 != "":

            float_qty = float(qty1)                 
            float_p_uni = float(p_uni1)

            somme  = format((float_qty  * float_p_uni), '.3f')

            #print(str(somme))
            self.ui.lineEdit_4.setText(str(somme))
        else:
            self.ui.lineEdit_4.setText("")

        return str(somme)

    def calc_remise(self):
            remise = self.ui.lineEdit_5
            p_tot = self.ui.lineEdit_4.text()

            #p_tot1 = str(p_tot.text())
            remise1 = str(remise.text())

            if p_tot != "" and remise1 != "":
                float_p_tot = float(p_tot)
                float_remise = float(remise1)

                self.outsider = format((float_p_tot - float_remise) + float(self.outsider), '.3f')
                #*net_p = net_p + self.outsider
                if float(self.outsider) >= 0.000:
                    self.ui.lineEdit_6.setText(str(self.outsider))
                else:
                    self.ui.lineEdit_6.setText("")
            return str(self.outsider)

    def calc_credit(self):

        p_tot = self.ui.lineEdit_6.text()
        remise = self.ui.lineEdit_7

        #p_tot.setValidator(QtGui.QDoubleValidator(0.999, 99.999, 3))


        #p_tot1 = str(p_tot.text())
        remise1 = str(remise.text())

        if remise1 != "" and p_tot != "":
            float_p_tot = float(p_tot)
            float_remise = float(remise1)

            net_p = format((float_p_tot - float_remise), '.3f')

            if float(net_p) >= 0.0:
                self.ui.lineEdit_8.setText(str(net_p))
            else:
                self.ui.lineEdit_8.setText("")

    def eventFilter(self, target, event):
        if target == self.ui.CB1 and event.type() == QtCore.QEvent.MouseButtonPress:
            self.fill_in_client()
        elif target == self.ui.CB2 and event.type() == QtCore.QEvent.MouseButtonPress:
            self.ui.CB2.clear()
            self.ui.CB2.addItems(["TISSU D'AMMEUBLEMENT", "RIDEAUX"]) 
        elif target == self.ui.CB3 and event.type() == QtCore.QEvent.MouseButtonPress: 
            self.handleOpenDialog()
        elif target == self.ui.CB3 and event.type() == QtCore.QEvent.KeyPress:
            self.ui.CB3.clear()
            self.ui.CB4.clear()
            self.fill_in_gamme()

        return False

    def fill_in_client(self):
            self.ui.CB1.clear()
            self.ui.CB1.addItems(get_list(db_cl_file))

    def fill_in_gamme(self):
            idx = get_index(db_gm_csv, 'VALIDE')
            #print(idx)
            self.ui.CB3.addItem(str(get_cl(db_gm_file, "db_gamme", 'B', 1931)[idx]))
            self.ui.CB4.addItem(str(get_cl(db_gm_file, "db_gamme", 'A', 1931)[idx]))
            if idx != "":
                os.remove(db_gm_csv)

    def reload(self):
        self.get_all(1)
        # self.ui.CB1.clear()
        # self.ui.CB2.clear()
        self.ui.CB3.clear()
        self.ui.CB4.clear()
        self.ui.lineEdit_1.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_4.clear()
        self.ui.lineEdit_5.clear()
        self.ui.lineEdit_6.clear()
        # self.ui.lineEdit_7.clear()
        # self.ui.lineEdit_8.clear()
        self.ui.rb1.setChecked(False)
        self.ui.rb2.setChecked(False)

    def get_all(self, idx):
        dt1 = date.today()
        dt_sort1 = dt1.strftime("%d_%b_%Y")
        dt = datetime.now()
        dt_sort = dt.strftime("%d/%m/%Y %H:%M:%S")
        
        dst_file = "./journalier/"+dt_sort1+".xlsx"
        # work_book = load_workbook(dst_file)
        # work_sheet = work_book.worksheets[0]
        
        try:
            if os.path.isfile(dst_file):
                if self.op == 0:
                    self.num = int(get_last_row(dst_file, 1)[0] + 1)
                    self.ind = int(get_last_row(dst_file, 1)[1])
            else:
                pass
        except OSError:
            pass
        
        cl = self.ui.CB1.currentText()
        rf = self.ui.CB2.currentText()
        gm = self.ui.CB3.currentText()
        cr = self.ui.CB4.currentText()
        qt = self.ui.lineEdit_1.text()
        mx = self.ui.lineEdit_2.text()
        pu = self.ui.lineEdit_3.text()  
        pt = self.ui.lineEdit_4.text()
        rm = self.ui.lineEdit_5.text()
        nt = self.ui.lineEdit_6.text()
        cd = self.ui.lineEdit_7.text()
        py = self.ui.lineEdit_8.text()

        ch = "Non_spécifié"
        if (self.ui.rb1.isChecked()):
            ch = "Espèce"
        elif (self.ui.rb2.isChecked()):
            ch = "Chèque"

        if idx == 0:
            if self.ui.chk.isChecked():
                if self.op != 0:
                    test = [None, None, None, gm, cr, qt, mx, pu, pt, rm, nt, cd, py, ch, dt_sort,"origine + replicate"]
                else:
                    test = [format(self.num, '04d'), cl, rf, gm, cr, qt, mx, pu, pt, rm, nt, cd, py, ch, dt_sort,"origine + replicate"]
                printing(0, dt_sort ,rf, nt, cd, py)
                printing(None, dt_sort+"\n_________replicate_________\n", rf, nt, cd, py)
            else:
                if self.op == 0:
                    test = [format(self.num, '04d'), cl, rf, gm, cr, qt, mx, pu, pt, rm, nt, cd, py, ch, dt_sort,"1xorigin"]
                else:
                    test = [None, None, None, gm, cr, qt, mx, pu, pt, rm, nt, cd, py, ch, dt_sort,"1xorigin"]
                printing(0 ,dt_sort ,rf, nt, cd, py)
                    
            set_jour(test, self.ind)    

        elif idx == 1:
            if self.op == 0:
                test = [format(self.num, '04d'), cl, rf, gm, cr, qt, mx, pu, pt, rm, nt, cd, None, None, dt_sort, "operation:"+str(self.op)]
            elif self.op != 0:
                test = [None, None, None, gm, cr, qt, mx, pu, pt, rm, nt, cd, None, None, dt_sort, "operation:"+str(self.op)]
            set_jour(test, self.ind)

        self.ind += 1
        self.op +=1
                

            

    def reload2(self):
        self.get_all(0)
        self.ui.CB1.clear()
        self.ui.CB2.clear()
        self.ui.CB3.clear()
        self.ui.CB4.clear()
        self.ui.lineEdit_1.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_4.clear()
        self.ui.lineEdit_5.clear()
        self.ui.lineEdit_6.clear()
        self.ui.lineEdit_7.clear()
        self.ui.lineEdit_8.clear()
        self.ui.rb1.setChecked(False)
        self.ui.rb2.setChecked(False)
        self.op = 0
        self.outsider = 0

    def handleOpenDialog(self):
        self.widget = MyTable()


if __name__ == '__main__':
    import sys
    pp = os.path.realpath("./db/")
    os.startfile(pp)
    app = QtWidgets.QApplication(sys.argv)
    mywidget = MyWidget()
    mywidget.show()
    sys.exit(app.exec_())