from PyQt4 import QtGui, QtCore


class MiFormulario(QtGui.QWidget):
    def __init__(self):
        super().__init__()
        self.init_GUI()

    def init_GUI(self):
        ''' Este m?todo inicializa la interfaz y sus elementos'''

        self.label1 = QtGui.QLabel('Texto:', self)
        self.label1.move(10, 15)

        self.label2 = QtGui.QLabel('Aqui se escribe la respuesta', self)
        self.label2.move(10, 50)

        self.edit1 = QtGui.QLineEdit('', self)
        self.edit1.setGeometry(45, 15, 100, 20)

        ''' agregamos la comunicaci?n del bot?n 1 con alg?n otro objeto'''
        self.boton1 = QtGui.QPushButton('&Procesar', self)
        self.boton1.resize(self.boton1.sizeHint())
        self.boton1.move(5, 70)
        self.boton1.clicked.connect(
            self.boton1_callback)  # La funci?n debe ser llamable. Esto es distinto que self.boton1_callback()

        self.boton2 = QtGui.QPushButton('&Salir', self)
        self.boton2.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.boton2.resize(self.boton2.sizeHint())
        self.boton2.move(90, 70)

        ''' Agrega todos los elementos al formulario '''
        self.setGeometry(200, 100, 200, 300)
        self.setWindowTitle('Ventana con Boton')

    def boton1_callback(self):
        ''' Este m?todo maneja el evento sobre quien opera'''
        self.label2.setText(self.edit1.text())


if __name__ == '__main__':
    app = QtGui.QApplication([])

    ''' Se crea una ventana descendiente de QMainWindows'''
    form = MiFormulario()
    form.show()
    app.exec_()
