from PyQt4 import QtGui
from gui import MainWindow

app = QtGui.QApplication([])
mainwindow = MainWindow()
mainwindow.show()
app.exec_()
