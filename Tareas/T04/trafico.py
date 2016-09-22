from random import choice, uniform, randint
from ciudad import Ciudad
from funciones import adyacentes, distancia, posicion_frente, per, suma, mul


class Transito:
    def __init__(self):
        self.mapa = []  ##
        self.vehiculos = {}
        self.calles = {}
        self.entradas = {}  # (ide, esquina)
        self.salidas = {}  # (pos)

    def agregar_auto(self):
        i, j = choice(list(self.entradas.keys()))
        direccion = self.calles[(i, j)].direccion
        x, y = suma((i, j), mul(-1, per(direccion)))

        try:
            if self.calles[x, y]:
                i, j = x, y
        except KeyError:
            pass

        self.vehiculos.update({(i, j): Vehiculo(i, j, direccion)})

    def mover_autos(self):

        tiempo_min = self._tiempo_minimo()
        lista_autos = list(self.vehiculos.values()).copy()
        for auto in lista_autos:
            # try:
            #    if auto.direccion in self._proxima_calle(auto).verde:
            #        self._mover_auto(auto, tiempo_min)
            # except AttributeError:  # Si llegamos aca es por que la siguiente calle no es una esquina
            self._mover_auto(auto, tiempo_min)

    def _mover_auto(self, vehiculo, tiempo):

        pos_anterior = vehiculo.i, vehiculo.j
        dist = vehiculo.velocidad * (tiempo + vehiculo.tiempo_restante)
        delta = round(dist)
        vehiculo.tiempo_restante = round((dist - delta) / vehiculo.velocidad, 2)

        vehiculo.i, vehiculo.j = suma((vehiculo.i, vehiculo.j), mul(delta, vehiculo.direccion))

        pos_nueva = vehiculo.i, vehiculo.j
        self.vehiculos.update({pos_nueva: vehiculo})
        del self.vehiculos[pos_anterior]

    def cruzar_autos(self):
        lista_autos = list(self.vehiculos.values()).copy()
        for auto in lista_autos:
            if type(self._proxima_calle(auto)) == Esquina:
                posiciones = self._posiciones_al_cruzar(auto)
                if posiciones:
                    pos_antigua = auto.i, auto.j
                    auto.i, auto.j = choice(posiciones)
                    auto.direccion = self.calles[auto.i, auto.j].direccion

                    del self.vehiculos[pos_antigua]
                    self.vehiculos.update({(auto.i, auto.j): auto})
                else:
                    print('Hay autos al frente no podemos cruzar')

    def _posiciones_al_cruzar(self, vehiculo):

        i, j = vehiculo.i, vehiculo.j
        dire_auto = vehiculo.direccion
        revisar_posiciones = [suma((i, j), mul(3, vehiculo.direccion))]

        try:
            pos_derecha = suma(suma((i, j), dire_auto), mul(-1, per(dire_auto)))
            direccion_cruce = self.calles[pos_derecha].direccion
            if direccion_cruce == mul(1, per(dire_auto)):
                print('Podemos cruzar a la derecha')
                revisar_posiciones.append(pos_derecha)
            else:
                pos_izquierda = suma(suma((i, j), mul(2, dire_auto)), mul(2, per(dire_auto)))
                try:
                    if self.calles[pos_izquierda]:
                        revisar_posiciones.append(pos_izquierda)
                except KeyError:
                    print('No hay nada a la izquierda')
                    pass

        except KeyError:
            print('No hay una calle a la derecha')
            pos_izquierda = suma(suma((i, j), mul(2, dire_auto)), mul(2, per(dire_auto)))
            direccion_cruce = self.calles[pos_izquierda].direccion
            if direccion_cruce == per(dire_auto):
                revisar_posiciones.append(pos_izquierda)


        # Ahora revisamos si es que en las posisicones hay algun auto
        lista = []
        for pos in revisar_posiciones:
            try:
                self.vehiculos[pos]
            except KeyError:
                lista.append(pos)
        print('posiciones posibles', lista)
        return lista

    def _tiempo_cruzar(self):
        tiempos = []
        for auto in self.vehiculos.values():
            if type(self.calles[posicion_frente(auto)]) == Esquina:
                tiempos.append(round(3 / auto.velocidad, 2) - auto.tiempo_restante)
        return min(tiempos)

    def _tiempo_minimo(self):
        """
        Calcula el tiempo minimo en el cuela un vehiculos se demora en llegar hasta algun cuadro justo
        antes de una esquina
        """
        tiempos = []
        for vehiculo in self.vehiculos.values():
            pos_auto = vehiculo.i, vehiculo.j
            i, j = vehiculo.i, vehiculo.j

            while type(self.calles[i, j]) != Esquina:
                i, j = suma((i, j), vehiculo.direccion)

            tiempo = round(distancia((i, j), pos_auto) / vehiculo.velocidad, 2) - vehiculo.tiempo_restante
            if tiempo > 0:
                tiempos.append(tiempo)
        try:
            return min(tiempos)
        except ValueError:
            return 0

    def _proxima_calle(self, vehiculo):
        """
        Retorna la calle que esta al frente del vehiculo siguiendo su direccion
        """
        return self.calles[suma((vehiculo.i, vehiculo.j), vehiculo.direccion)]

    def _encontrar_esquinas(self):
        for calle in self.calles.values():
            i, j = calle.i, calle.j

            try:  ## Arreglar puede que acepte cosas que no quiero
                if (self.mapa[i][j - 1] == 'C' and self.mapa[i][j + 1] == 'E') or (
                                self.mapa[i][j - 1] == 'E' and self.mapa[i][j + 1] == 'C') or (
                                self.mapa[i - 1][j] == 'C' and self.mapa[i + 1][j] == 'E') or (
                                self.mapa[i - 1][j] == 'E' and self.mapa[i + 1][j] == 'E'):
                    self.mapa[i][j] = 'E'
                    self.calles.update({(i, j): Esquina(i, j, calle.direccion)})
            except IndexError:
                self.mapa[i][j] = 'E'
                self.calles.update({(i, j): Esquina(i, j, calle.direccion)})

    def _vecinos(self, objeto):

        i, j = objeto.i, objeto.j
        lista = []
        for n in {1, -1}:
            try:
                lista.append(self.calles[i + n, j])
            except KeyError:
                pass
        for n in {1, -1}:
            try:
                lista.append(self.calles[i, j + n])
            except KeyError:
                pass
        return lista

    def set_mapa(self, ciudad):

        dim = ciudad.dim
        self.mapa = [['_' for _ in range(dim[1])] for _ in range(dim[0])]

        for i in range(dim[0]):
            for j in range(dim[1]):
                objeto = ciudad.plano[i][j]
                if repr(objeto) == 'Casa':
                    self.mapa[i][j] = 'C'  # Casa

                if repr(objeto) == 'Calle':
                    vecinos = adyacentes(objeto, ciudad.plano)

                    if all(map(lambda x: x == 'Calle', vecinos)) and len(vecinos) == 4:
                        self.mapa[i][j] = 'E'  # Esquina
                        self.calles.update({(i, j): Esquina(i, j, objeto.direccion)})
                    else:
                        self.mapa[i][j] = 'T'  # Calle Normal
                        self.calles.update({(i, j): Calle(i, j, objeto.direccion)})

        self._encontrar_esquinas()
        self._encontrar_esquinas()
        # self._agregar_direciones()

        for calle in [calle for ((i, j), calle) in self.calles.items() if i == 0]:
            i, j = calle.i, calle.j
            if calle.direccion == (1, 0):
                self.entradas.update({(i, j): calle})
            if calle.direccion == (-1, 0):
                self.salidas.update({(i, j): calle})

        for calle in [calle for ((i, j), calle) in self.calles.items() if j == 0]:
            i, j = calle.i, calle.j
            if calle.direccion == (0, 1):
                self.entradas.update({(i, j): calle})
            if calle.direccion == (0, -1):
                self.salidas.update({(i, j): calle})

        for calle in [calle for ((i, j), calle) in self.calles.items() if i == dim[0] - 1]:
            i, j = calle.i, calle.j
            if calle.direccion == (-1, 0):
                self.entradas.update({(i, j): calle})
            if calle.direccion == (1, 0):
                self.salidas.update({(i, j): calle})

        for calle in [calle for ((i, j), calle) in self.calles.items() if j == dim[1] - 1]:
            i, j = calle.i, calle.j
            if calle.direccion == (0, -1):
                self.entradas.update({(i, j): calle})
            if calle.direccion == (0, 1):
                self.salidas.update({(i, j): calle})


class Calle:
    def __init__(self, i, j, direccion):
        self.i = i
        self.j = j
        self.direccion = direccion

    def __repr__(self):
        return 'C: ({0},{1})'.format(self.i, self.j)


class Esquina(Calle):
    def __init__(self, i, j, direccion):
        super().__init__(i, j, direccion)
        self.direcciones = [direccion]
        self.verde = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        self.color_horinzontal = False

    def __repr__(self):
        return 'E'


class Vehiculo:
    n = 1

    def __init__(self, i, j, direccion):
        self.i = i
        self.j = j
        self.velocidad = round(uniform(0.5, 1), 1)
        self.direccion = direccion
        self.tiempo_restante = 0
        self.ide = self.n
        Vehiculo.n += 1

    @property
    def dobla(self):
        return randint(0, 1)

    def __repr__(self):
        return 'Auto: {0}, Pos: ({1},{2})'.format(
            self.ide, self.i, self.j)


if __name__ == '__main__':
    city = Ciudad()
    city.cargar_plano('/home/ivanwolf/ivanwolf15-repo/Tareas/T04/mapa fix.txt')
    transito = Transito()
    transito.set_mapa(city)
    # for calle in transito.calles.values():
    #    if type(calle) == Esquina:
    #        print(len(calle.direcciones), calle.direcciones)


    transito.agregar_auto()
    print(list(transito.vehiculos.values()))
    transito.mover_autos()
    print(list(transito.vehiculos.values()))
    transito.cruzar_autos()
    print(list(transito.vehiculos.values()))
    transito.mover_autos()
    print(list(transito.vehiculos.values()))
    transito.cruzar_autos()
    print(list(transito.vehiculos.values()))
    transito.mover_autos()
    print(list(transito.vehiculos.values()))
    # transito.agregar_auto()
    # print(list(transito.vehiculos.values()))
    # transito.mover_autos()
    # print(list(transito.vehiculos.values()))
