import sys
from PyQt4 import QtGui
from backend import Partida


class Buscaminas(QtGui.QWidget):
    def __init__(self, n, minas):  # con "n" se genera una matriz de nxn
        super(Buscaminas, self).__init__()
        self.n = n
        self.minas = minas
        self.partida = Partida(n, minas)
        # posiciones = [(i, j) for i in range(self.n) for j in range(self.n)]
        self.botones = dict()
        ":::COMPLETAR:::"

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Buscaminas')
        self.setGeometry(200, 100, 400, 500)

        grilla = QtGui.QGridLayout()
        self.setLayout(grilla)

        for posicion in [(i, j) for i in range(self.n) for j in range(self.n)]:
            boton = QtGui.QPushButton()
            boton.setFixedSize(50, 50)
            boton.clicked.connect(self.buttonClickedLeft)
            self.botones.update({boton: posicion})
            grilla.addWidget(boton, *posicion)

        self.label = QtGui.QLabel('', self)
        self.label.move(0, 0)
        self.label.setFixedSize(200, 60)


    def buttonClickedLeft(self):
        sender = self.sender()
        posicion = self.botones[sender]
        texto = self.apretar_boton(posicion)
        if sender.text() == '':

            if texto == 'X':
                sender.setText(texto)
                self.notificar('El espia ha muerto  ')
                print('hola')
            else:
                sender.setText(texto)

    def apretar_boton(self, posicion):  # Posición como una tupla (x, y)
        "Esta funcion devuelve la cantidad de minas alrededor de un espacio"
        "No tiene ninguna relación con lo que sucederá en la UI"
        boton = self.partida.botones[posicion]
        return self.partida.clickear(boton)

    def notificar(self, mensaje):
        self.label.setText(mensaje)
        "Debe notificar a traves de un label cuando muera o sobreviva"


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Buscaminas(5, 10)
    ex.show()
    sys.exit(app.exec_())
