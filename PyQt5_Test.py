import sys
from PyQt5.QtWidgets import (QApplication,QWidget,QPushButton,QDesktopWidget, QLineEdit, QInputDialog)
from PyQt5.QtCore import QCoreApplication

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        self.btn1 = QPushButton('Quit', self)
        self.btn1.move(420, 300)
        self.btn1.resize(self.btn1.sizeHint())
        self.btn1.clicked.connect(QCoreApplication.instance().quit)

        self.btn2 = QPushButton('IP Input', self)
        self.btn2.move(30, 30)
        self.btn2.clicked.connect(self.showDialog)

        self.btn3 = QPushButton('IP Input2', self)
        self.btn3.move(30, 90)
        self.btn3.clicked.connect(self.showDialog2)

        self.le = QLineEdit(self)
        self.le.move(120, 30)

        self.le2 = QLineEdit(self)
        self.le2.move(120, 90)

        self.setWindowTitle('System Check')
        self.resize(500,350)
        self.center()
        self.show()


    def showDialog(self):
        IP1,ok = QInputDialog.getInt(self,'Input IP','Enter your IP:')
        
        if ok:
            self.le.setText(str(IP1))
        return IP1    

    def showDialog2(self):
        IP1,ok = QInputDialog.getInt(self,'Input IP','Enter your IP:')
        
        if ok:
            self.le2.setText(str(IP1))
        return IP1            
           
           


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())