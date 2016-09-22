from algoritmos import bfs, backtrack, doble_sentido
from estructuras import Lista, Dict, Tupla


class Red:
    def __init__(self):
        self.puertos = Dict(50)

    def agregar_puerto(self, puerto_actual, puerto_anterior=None, m=None, atrapado=False):
        if self.puertos:
            if not atrapado:
                puerto_anterior.agregar_vecino(puerto_actual, m)

        if puerto_actual.ide not in self.puertos:
            self.puertos[puerto_actual.ide] = puerto_actual

    def obtener_conexiones(self):
        lista_conexiones = Lista()
        for m in self.puertos:

            for (u, vecino) in self.puertos[m].vecinos.items:
                if len(vecino) >= 3:
                    for v in vecino:
                        lista_conexiones.append(Tupla(m, v, 'RAND'))
                elif len(vecino) == 2:
                    for v in vecino:
                        lista_conexiones.append(Tupla(m, v, 'ALT'))
                elif len(vecino) == 1:
                    for v in vecino:
                        lista_conexiones.append(Tupla(m, v, ''))
        return lista_conexiones

    def ruta_a_bummer(self):
        g = self.puertos.values
        bfs(g, self.puerto_inicial)
        return backtrack(self.puerto_bummer)

    def imprimir_prueba(self):
        """
        Esta funcion guarda en un archivo de texto informacion acerca de los puertos, por ejemplo ver sus vecinos,
        cuantas veces se visito un puerto, si esta completo, etc
        """
        file = open('data/test.txt', 'w+')
        for puerto in self.puertos.values:
            linea = 'ID{0}, Vecinos: {1}, Completo: {3}, Conexion: {2}\n'.format(puerto.ide, puerto.vecinos,
                                                                                 puerto.conexion, puerto.completo)
            file.write(linea)
        file.close()

    def imprimir_red(self):
        file = open('data/red.txt', 'w+')
        s1 = ''
        s2 = ''
        for m in self.puertos:
            s1 += 'PUERTO {0} \n'.format(m)
        for conexion in self.obtener_conexiones():
            s2 += 'CONEXION {0} {1} {2} \n'.format(conexion[0], conexion[1], conexion[2])
        file.write(s1)
        file.write(s2)
        file.close()
        print("Red guardada en 'data/red.txt' ")

    def imprimir_ruta(self):
        file = open('data/rutaABummer.txt', 'w+')
        ruta = list(reversed(self.ruta_a_bummer()))

        for i in range(len(ruta) - 1):
            file.write('CONEXION ID{0} ID{1} \n'.format(ruta[i], ruta[i + 1]))

        file.close()
        print("Ruta mas corta guardada en 'data/rutaABummer.txt' ")

    def imprimir_rutas_dobles(self):

        pares = doble_sentido(self.puertos.values)

        file = open('data/rutasDobleSentido.txt', 'w+')
        for par in pares:
            if len(par) == 2:
                file.write('PAR {0} {1} \n'.format(par[0], par[1]))
            elif len(par) > 2:
                s = ''
                for ide in par:
                    s += '{0} '.format(ide)
                file.write('RUTA ' + s + '\n')
        if not pares:
            file.write('NO ENCONTRAMOS NINGUNA RUTA EN DOBLE SENTIDO \n')
        print("Rutas dobles guardadas en 'data/rutasDobleSentido.txt' ")
        file.close()

    @property
    def puerto_inicial(self):
        return self.puertos[0]

    @property
    def puerto_bummer(self):
        for puerto in self.puertos.values:
            if puerto.bummer:
                return puerto


class Puerto:
    def __init__(self, ide, posibles, capacidad):
        self.ide = ide
        self.posibles = posibles
        self.capacidad = capacidad
        self.vecinos = Dict(50)
        self.conexion = 0
        self.bummer = False

        # Atributos necesarios para usar los algoritmos de grafos

        self.padre = None
        self.distancia = None
        self.visto = None
        self.calculado = False

    def __eq__(self, other):
        if isinstance(other, Puerto):
            if self.ide == other.ide:
                return True
        return False

    def __repr__(self):
        return '{0}'.format(self.ide)

    def agregar_vecino(self, puerto, m):
        if m in self.vecinos:
            if puerto not in self.vecinos[m]:
                self.vecinos[m].append(puerto)
        else:
            self.vecinos[m] = [puerto]

    @property
    def completo(self):
        """
        Propiedad que indica si es que desde un puerto u se paso por lo menos a todas las conexiones posibles
        de u, sirve para poder ver el estado de la red
        :return: Bool
        """
        if self.posibles == len(self.vecinos):
            return True
        return False

    @property
    def proxima_conexion(self):
        """
        Calcula la porxima conexion que se hara cuando se vuelva a pasar por el puerto self
        :return: Int
        """
        n = self.conexion % self.posibles
        self.conexion += 1
        return n

    @property
    def lista_vecinos(self):
        """
        Retorna una lista de objetos tipo Puerto con los puertos adyacentes a self
        :return: Lista
        """
        lista_vecinos = Lista()
        for lista in self.vecinos.values:
            for vecino in lista:
                if vecino not in lista_vecinos:
                    lista_vecinos.append(vecino)
        return lista_vecinos
