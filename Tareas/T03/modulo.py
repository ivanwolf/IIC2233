from funciones import esta_en_el_tablero


class Tablero:
    def __init__(self, largo=None, jugador=None):
        self.largo = largo
        self.jugador = jugador
        self.piezas = []
        self.grilla = [[[None, None] for _ in range(largo)] for _ in range(largo)]

    def __getitem__(self, item):
        return self.grilla[item[0]][item[1]][item[2]]

    def __setitem__(self, item, value):
        self.grilla[item[0]][item[1]][item[2]] = value

    def ubicar_vehiculo(self, pos, vehiculo):
        """
        Intenta agregar el vehiculo en la posicion pos, manejando las exepciones. Si se ubica el vehiculo con exito,
        se agrega el ataque especial del vehiculo al arsenal del jugador dueno del tablero
        :param pos: Tuple (x,y,z)
        :param vehiculo: Vehiculo Object
        :return: Bool
        """

        posible_ubicacion = [(pos[0] + q[0], pos[1] + q[1], q[2]) for q in vehiculo.area]
        self._ubicacion_valida(posible_ubicacion, vehiculo)

        vehiculo.posicion_cabeza = pos

        for (x, y, z) in vehiculo.ubicacion:
            self[x, y, z] = vehiculo

        print('{0} ubicado correctamente'.format(vehiculo))

        self.piezas.append(vehiculo)
        self.jugador.vehiculos.append(vehiculo)
        ataque = vehiculo.ataque_unico
        if ataque is not None:
            self.jugador.arsenal.update({repr(ataque): ataque})

        return True

    def mover_vehiculo(self, pos, vehiculo):

        if vehiculo.movimientos_posibles is None:
            print('El puerto no se puede mover, intentalo otra vez')
            raise PermissionError

        elif vehiculo.movimientos_posibles == 'All':
            posible_ubicacion = [(pos[0] + q[0], pos[1] + q[1], q[2]) for q in vehiculo.area]

        else:
            if pos in vehiculo.movimientos_posibles:
                posible_ubicacion = [(pos[0] + q[0], pos[1] + q[1], q[2]) for q in vehiculo.area]

            else:
                print('Solo nos podemos mover una casilla a la vez!, intentalo otra vez')
                raise RuntimeError

        self._ubicacion_valida(posible_ubicacion, vehiculo)

        for (x, y, z) in vehiculo.ubicacion:
            self[x, y, z] = None

        vehiculo.posicion_cabeza = pos

        for (x, y, z) in vehiculo.ubicacion:
            self[x, y, z] = vehiculo

        print('Movimiento realizado con exito, nueva posicion de {0}: {1}'.format(vehiculo.name, pos))
        return True

    def _quitar_vehiculo(self, vehiculo):
        try:
            self.piezas.remove(vehiculo)
            print('Nuestro {} ha sido destruido'.format(vehiculo.name))
            for pos in vehiculo.ubicacion:
                self[pos] = None
                try:
                    if self.jugador.__class__.__name__ == 'Jugador':
                        self.jugador.oponente.radar.marcar('U', (pos[0], pos[1]))  # Marca el radar del enemigo
                except AttributeError:
                    pass
        except ValueError:
            pass

        try:
            del self.jugador.arsenal[repr(vehiculo.ataque_unico)]
        except KeyError:
            pass

    def _ubicacion_valida(self, ubicacion, vehiculo):
        """
        :param ubicacion: Lista con posiciones (x,y,z)
        :param vehiculo: Vehiculo()
        :raises: RuntimeError, IndexError
        """
        for q in ubicacion:
            if not esta_en_el_tablero(q, self.largo):
                print('Una coordenanda del vehiculo queda afuera del tablero')
                raise IndexError
            if self[q] != vehiculo:
                if self[q]:
                    print('La posicion {0} ya esta siendo ocupada'.format(q))
                    raise RuntimeError

    def revisar_piezas(self):
        """
        Inspecciona las piezas del tablero y determina si es que es necesario eliminarlas
        """
        for vehiculo in self.piezas:

            if vehiculo.napalm:
                vehiculo.resistencia -= 5
                self.jugador.dano_total_recibido += 5
                self.jugador.oponente.dano_total_causado += 5
                vehiculo.napalm = False

            try:
                if vehiculo.resistencia <= 0:
                    self._quitar_vehiculo(vehiculo)
                    self.jugador.oponente.nota = vehiculo
            except TypeError:  # Los aviones no tienen resistencia
                pass

    def imprimir(self, k=0):
        """
        Muestra en consola el estado actual del tablero k
        :param k: int, si k = 0 se muestra el tablero maritimo, si k = 1 se muestra el aereo
        """

        # if isinstance(self.jugador, Computador):
        #    return True
        x = ['' + ' {} '.format(n).rjust(2) + '' for n in range(self.largo)]
        table = [['  ' for _ in range(self.largo)] for _ in range(self.largo)]
        for i in range(self.largo):
            for j in range(self.largo):
                if self[i, j, k]:
                    table[j][i] = self[i, j, k]

        if k == 0:
            print('#### Tablero \n')
        elif k == 1:
            print(' ### Tablero Aereo \n')

        print('   | ' + '| '.join(x) + '|\n')

        for row in enumerate(table):
            print(
                '{}'.format(row[0]).rjust(2) + ' | ' +
                ' | '.join('{}'.format(column) for column in row[1]) + ' |\n')
        print('\n')

    def imprimir_piezas(self):
        """
        Muestra en consola el estado de los vehiculos
        """
        print('Vehiculos: ')
        for item in enumerate(self.piezas):
            print('[{}]: '.format(item[0]) +
                  '{}'.format(item[1].name).ljust(16) +
                  '- HP: {}'.format(item[1].resistencia))
        print('')

    def imprimir_arsenal(self):
        n = self.jugador.turno

        print('Ataques disponibles: ')
        for item in self.jugador.arsenal.items():
            disp = item[1].disponible(n)
            if disp[0]:
                print('[{0}]: {1}'.format(item[0], item[1].name))
            else:
                print('[XX]: {0}, Disponible en {1} turnos'.format(item[1].name, disp[1]))

    def imprimir_historial(self):
        if not self.jugador.historial:
            print('Aun no hemos atacado \n')
            raise AssertionError
        else:
            for line in self.jugador.historial:
                print(line)

    def imprimir_turno(self):
        n = self.jugador.turno
        print('##################')
        print('Turno {}, Jugador {}'.format(n, self.jugador.name))
        print('##################')
        print('\n')

    @staticmethod
    def imprimir_menu():

        print('Menu: ')
        print('[0]: Mostrar Historial')
        print('[1]: Mover vehiculo')
        print('[2]: Atacar')
        print('[3]: Explorar')
        print('[4]: Rendirse')

    @staticmethod
    def imprimir_lineas():
        for i in range(10):
            print('\n')


class Radar:
    def __init__(self, largo=0, jugador=None):
        self.largo = largo
        self.jugador = jugador
        self.registro = {}
        self.hits = []
        self.miss = []
        self.grilla = [[' ' for _ in range(largo)] for _ in range(largo)]

    def __getitem__(self, item):
        return self.grilla[item[0]][item[1]]

    def __setitem__(self, item, value):
        self.grilla[item[0]][item[1]] = value

    def equivalentes(self, other):

        for i in range(self.largo):
            for j in range(self.largo):
                if self[i, j] != other[i, j]:
                    return False
        return True

    def marcar(self, marca, pos):
        x, y = pos[0], pos[1]
        self[y, x] = marca
        if marca == 'X':
            self.miss.append((x, y))
        if marca == 'O':
            self.hits.append((x, y))

    def imprimir(self):
        try:
            n = self.jugador.turno
            print('### Radar Turno {} \n'.format(n))
        except AttributeError:
            pass
        x = ['' + '{}'.format(n).rjust(2) + '' for n in range(self.largo)]
        table = self.grilla

        print('   | ' + '| '.join(x) + '| ')

        for row in enumerate(table):
            print(
                '{}'.format(row[0]).rjust(2) + ' | ' + ' | '.join('{}'.format(column) for column in row[1]) + ' | ')
        print('\n')

    def copy(self):
        other = Radar(largo=self.largo)
        for i in range(self.largo):
            for j in range(self.largo):
                if self[i, j] != ' ':
                    other.marcar(self[i, j], (j, i))
        return other
