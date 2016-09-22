from PyQt4 import QtGui, uic
from calc_financiero import calcular_jub

form = uic.loadUiType("hexa.ui")


class MainWindow(form[0], form[1]):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        img_arg = QtGui.QPixmap('logo_argentum.png')
        img_hexa = QtGui.QPixmap('logo_hexa.png')
        self.label_1.setPixmap(img_arg)
        self.label_2.setPixmap(img_hexa)
        # Completar la creación de la interfaz #
        self.input1.textChanged.connect(self.calcular)

        self.input2.textChanged.connect(self.calcular)

        self.input3.textChanged.connect(self.calcular)

        self.input4.textChanged.connect(self.calcular)
        self.input5.textChanged.connect(self.calcular)
        self.combobox.currentIndexChanged.connect(self.calcular)

    def calcular(self):
        """ Completar esta función para calcular los cambios de los datos
        en tiempo real según el input del usuario. """
        if self.input1.text() and self.input2.text() and self.input3.text() and self.input4.text() and self.input5.text():
            ingreso = int(self.input1.text())
            cotiza = int(self.input2.text())
            edad = int(self.input3.text())
            edad_j = int(self.input4.text())
            esp_vida = int(self.input5.text())
            fondo = self.combobox.itemText(self.combobox.currentIndex())
            self.calculo_label.setText(calcular_jub(ingreso, cotiza, edad, edad_j, esp_vida, fondo))
            self.aporte_label.setText(str(ingreso * cotiza/100))
            self.pension_label.setText(str(esp_vida - edad))
        else:
            pass



if __name__ == '__main__':
    app = QtGui.QApplication([])
    form = MainWindow()
    form.show()
    app.exec_()
