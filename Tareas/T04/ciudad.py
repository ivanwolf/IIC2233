from random import random, uniform
from PyQt4 import QtGui
from gui.gui import GrillaSimulacion


class Ciudad:
    def __init__(self):
        self.plano = []
        self.trafico = []
        self.dim = (0, 0)
        self.espacios_vacios = []

    def cargar_plano(self, path):
        with open(path, 'r') as file:
            first_line = file.readline()
            self.dim = int(first_line.split('x')[0]), int(first_line.split('x')[1])
            lineas = file.readlines()

        self.plano = [['_' for _ in range(self.dim[1])] for _ in range(self.dim[0])]

        for linea in lineas:
            aux = linea.replace(' ', '$', 1)
            i, j = int(aux.split('$')[0].split(',')[0]), int(aux.split('$')[0].split(',')[1])

            if 'casa' in linea:
                ind = linea.index('de') + 3
                aux = linea[ind:].replace(' ', '#', 1).split('#')
                material = aux[0]
                tiempo = aux[1].lstrip('[').rstrip(']\n').split(',')
                tiempo_robos = (int(tiempo[0]), int(tiempo[1]))

                self.plano[i][j] = Casa(i, j, material, tiempo_robos)

            if 'calle' in linea:
                ind = linea.index(' ', 6) + 1
                direccion = linea[ind:-1]
                if direccion == 'arriba':
                    self.plano[i][j] = Calle(i, j, (-1, 0))
                if direccion == 'abajo':
                    self.plano[i][j] = Calle(i, j, (1, 0))
                if direccion == 'derecha':
                    self.plano[i][j] = Calle(i, j, (0, 1))
                if direccion == 'izquierda':
                    self.plano[i][j] = Calle(i, j, (0, -1))

            if 'vacio' in linea:
                self.espacios_vacios.append((i, j))
                self.plano[i][j] = 'V'


class Calle:
    def __init__(self, i, j, direccion):
        self.i = i
        self.j = j
        self.direccion = direccion

    def __repr__(self):
        return 'Calle'


class Casa:
    def __init__(self, i, j, material, tiempo_robos):
        self.i = i
        self.j = j
        self.material = material
        self.tiempo_robos = tiempo_robos

    def __repr__(self):
        return 'Casa'

