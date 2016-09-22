from PyQt4 import QtGui
from gui.gui import GrillaSimulacion
from ciudad import Ciudad, Calle, Casa
from trafico import Transito

def mostrar_plano(ciudad):

    app = QtGui.QApplication([])
    grilla_simulacion = GrillaSimulacion(app, ciudad.dim[1], ciudad.dim[0])
    grilla_simulacion.show()

    for i in range(ciudad.dim[0]):
        for j in range(ciudad.dim[1]):

            if type(ciudad.plano[i][j]) is Casa:
                grilla_simulacion.agregar_casa(i + 1, j + 1)
            if type(ciudad.plano[i][j]) is Calle:
                grilla_simulacion.agregar_calle(i + 1, j + 1)


    app.exec_()

def mostrar_trafico():
    pass

if __name__ == '__main__':
    city = Ciudad()
    city.cargar_plano('/home/ivanwolf/ivanwolf15-repo/Tareas/T04/mapa fix.txt')

    transito = Transito()
    transito.set_mapa(city)

    mostrar_plano(city)