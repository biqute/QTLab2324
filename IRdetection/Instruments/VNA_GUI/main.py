from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys



class mywindow(QMainWindow): #We are going to inherit QMainWindow properties and change them slightley
    def __init__(self):
        super(mywindow, self).__init__()
        self.setGeometry(200,200,300,300)
        self.setWindowTitle('My first window')
        self.initUI()

    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText('My first label')
        self.label.move(100,100)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText('Click Here!')
        self.b1.clicked.connect(self.clicked)

    def clicked(self):
        self.label.setText('Button pressed')
        self.update()
        
    def update(self):
        self.label.adjustSize()


def window():
    app = QApplication(sys.argv)
    win = mywindow()
    win.show()
    sys.exit(app.exec_())

window()
