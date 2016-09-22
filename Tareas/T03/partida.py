import time
import random
from funciones import ask_fila, ask_position, loop, ask_number, ask_attack
from vehiculo import BuquedeGuerra, BarcoPequeno, Lancha, Puerto, AvionExplorador, Kamikaze, AviondeCaza
from ataque import AtaqueNormal, Ingenieros, Paralizador, MisildeCrucero
from jugador import Jugador, Computador


class Partida:
    tipos_de_piezas = [Lancha, BuquedeGuerra, BarcoPequeno, Puerto, AvionExplorador, Kamikaze, AviondeCaza]

    def __init__(self):
        self.jugador1 = Jugador()
        self.jugador2 = Jugador()

    def login(self):
        print('Bienvendido a Bummer UC ')
        print('[0]: 1 Jugador')
        print('[1]: 2 Jugadores')

        choice = loop(ask_number, [2], (IndexError, ValueError), '', '')

        if choice == 1:
            print('Dimension del tablero: ')
            n = loop(ask_number, [12], (IndexError, ValueError), '', '')
            self.jugador1 = Jugador(input('Nombre Jugador 1: \n'), n)
            self.jugador2 = Jugador(input('Nombre Jugador 2: \n'), n)
        else:
            self.jugador1 = Jugador(input('Nombre Jugador 1: \n'), 8)
            self.jugador2 = Computador('Computador 1', 8)

        self.jugador1.oponente = self.jugador2
        self.jugador2.oponente = self.jugador1

    def turno_cero(self, jugador):
        """
        Comienza el juego, ubicando las piezas del jugador en el tablero y agregando el ataque normal
        al arsenal del jugador.
        :param  jugador: Jugador()
        """
        jugador.arsenal.update({'AN': AtaqueNormal()})
        tablero = jugador.tablero
        l = tablero.largo

        print('{0} esta ubicando sus piezas \n'.format(jugador.name))

        if isinstance(jugador, Computador):
            print('La computadora esta ubicando sus piezas')
            for clase in self.tipos_de_piezas:
                vehiculo = clase()
                k = vehiculo.k
                go = True
                while go:
                    try:
                        tablero.ubicar_vehiculo((random.randint(0, l - 1), random.randint(0, l - 1), k), vehiculo)
                        go = False
                    except (RuntimeError, IndexError):
                        pass
            jugador.turno += 1
            time.sleep(1.2)
            return True

        for clase in self.tipos_de_piezas:
            vehiculo = clase()
            area = vehiculo.area_utilizada
            k = vehiculo.k
            tablero.imprimir(k)
            print('{0}'.format(jugador.name))
            print('{0}, Area: {1}x{2}'.format(vehiculo.name, area[0], area[1]))
            msg = 'Donde nos ubicamos? Posicion x,y : '
            error = ''
            pos = loop(ask_position, [k, l], (ValueError, KeyError, IndexError), msg, error)
            go = True
            while go:
                try:
                    tablero.ubicar_vehiculo(pos, vehiculo)
                    go = False
                except (RuntimeError, IndexError):
                    pos = loop(ask_position, [k, l], (ValueError, KeyError, IndexError), msg, error)

        print('Piezas ubicadas correctamente! \n')

        tablero.imprimir_lineas()
        jugador.turno += 1
        time.sleep(1.2)

    @staticmethod
    def turno_computador(jugador):

        if jugador.primer_movimiento():
            time.sleep(1.2)
            jugador.turno += 1
            return True

        jugador.podar()
        pos = jugador.pensar()
        print('El computador eligio la posicion {}'.format(pos))
        ataque = jugador.arsenal['AN']
        jugador.atacar(ataque, pos)
        jugador.ultimo_ataque = pos[0], pos[1]

        time.sleep(1.2)
        jugador.turno += 1

        return True

    @staticmethod
    def sorteo(jugadores):
        print('Realizando el sorteo ')
        result = jugadores
        if random.randint(0, 1) == 1:
            result = [jugadores[1], jugadores[0]]
        print('#####')
        print('Comienza el juego {}'.format(result[0]))
        print('##### \n')
        return result

    def turno(self, jugador):
        """
        Un turno normal dentro del juego
        :param jugador: Jugador()
        """
        tablero = jugador.tablero
        radar = jugador.radar
        n = tablero.largo
        print('\n####### \n')

        tablero.imprimir_turno()
        tablero.revisar_piezas()

        if jugador.defeated:
            print('Te has quedado sin barcos, GG\n')
            print('\n#########')
            print('El ganador es {}'.format(jugador.oponente))
            print('#########\n')
            return False

        if isinstance(jugador, Computador):
            return self.turno_computador(jugador)

        if jugador.revelar:
            print('## Atencion')
            print('Una coordenada del avion explorador enemigo es {}\n'.format(jugador.revelar))
            jugador.revelar = False

        click = -1
        tablero.imprimir(0)
        tablero.imprimir_piezas()
        tablero.imprimir_menu()

        while click == -1:

            click = loop(ask_number, [5], (IndexError, ValueError), '', '')

            # 0 Mostrar Historial
            # 1 Mover vehiculo
            # 2 Atacar
            # 3 Explorar
            # 4 Rendirse

            if click == 0:
                try:
                    tablero.imprimir_historial()
                    print('Elegir turno para mostrar el radar: ')
                    r = loop(ask_number, [n], (IndexError, ValueError), '', '')
                    try:
                        jugador.lista_radares[r-1].imprimir()
                    except IndexError:
                        pass
                except AssertionError:
                    click = -1
                    tablero.imprimir_menu()

            elif click == 1:
                print('Escoger un vehiculo: ')
                tablero.imprimir_piezas()
                m = loop(ask_number, [len(tablero.piezas)], (IndexError, ValueError), '', '')
                vehiculo = tablero.piezas[m]
                k = vehiculo.k

                msg = 'Donde nos moveremos?'
                error = 'Necesitamos ordenes claras!'
                pos = loop(ask_position, [k, n], (ValueError, KeyError, IndexError), msg, error)

                go = True
                while go:
                    try:

                        tablero.mover_vehiculo(pos, vehiculo)
                        go = False
                    except RuntimeError:
                        pos = loop(ask_position, [k, n], (ValueError, KeyError, IndexError), msg, error)
                    except PermissionError:
                        go = False
                        click = -1
                        tablero.imprimir_menu()
            elif click == 2:

                tablero.imprimir_arsenal()
                msg = 'Coordenadas del ataque x,y: '
                msg2 = 'Que ataque usaremos? (ingresar siglas) \n'
                error = 'El formato valido para las posiciones es x,y '

                ataque = loop(ask_attack, [jugador.arsenal, jugador.turno], (KeyError, PermissionError), msg2)

                if isinstance(ataque, Ingenieros):
                    tablero = jugador.tablero
                    msg = 'Escoger un vehiculo para reparar: '
                    error = 'Crep que ingresaste un str o un numero muy grande'
                    n = tablero.largo
                    tablero.imprimir_piezas()

                    m = loop(ask_number, [n], (IndexError, ValueError), msg, error)
                    vehiculo = tablero.piezas[m]
                    jugador.usar_ingenieros(ataque, vehiculo)

                    print('Fin del turno\n')
                    jugador.turno += 1
                    return True

                elif isinstance(ataque, Paralizador):
                    m1 = 'Primera coordenada del paralizador \n'
                    m2 = 'Segunda coordenada del paralizador \n'
                    error = 'El formato valido para las posiciones es x,y '

                    pos1 = loop(ask_position, [1, n], (ValueError, KeyError, IndexError), m1, error)
                    pos2 = loop(ask_position, [1, n], (ValueError, KeyError, IndexError), m2, error)
                    jugador.usar_paralizador(ataque, pos1, pos2)

                    print('Fin del turno\n')
                    jugador.turno += 1
                    return True

                elif isinstance(ataque, MisildeCrucero):
                    msg = 'A que fila o columna atacamos? ej: f,4 o c,2 \n'
                    exepciones = (KeyError, IndexError, ValueError)
                    radar.imprimir()
                    inp = loop(ask_fila, [n], exepciones, msg)
                    jugador.usar_misil_de_crucero(ataque, inp)
                    jugador.turno += 1
                    return True

                radar.imprimir()
                pos = loop(ask_position, [0, n], (ValueError, KeyError, IndexError), msg, error)
                jugador.atacar(ataque, pos)

            elif click == 3:
                msg = 'Posicion a explorar? '
                error = 'Necesitamos ordenes claras!'
                radar.imprimir()
                pos = loop(ask_position, [0, n], (ValueError, KeyError), msg, error)
                try:
                    jugador.explorar(pos)
                except PermissionError:
                    click = -1
                    tablero.imprimir_menu()

            elif click == 4:
                jugador.surrender = True
                return False

        print('Fin del turno\n')
        jugador.lista_radares.append(radar.copy())
        jugador.turno += 1
        time.sleep(1.2)
        return True

    def jugar(self):

        self.login()
        jugadores = [self.jugador1, self.jugador2]
        for jugador in jugadores:
            self.turno_cero(jugador)

        jugadores = self.sorteo(jugadores)

        while True:
            for jugador in jugadores:
                if not self.turno(jugador):
                    self.imprimir_stats()
                    return False

    """ Stats """

    @staticmethod
    def _barco_con_mas_movimientos(jugador):

        barcos = [vehiculo for vehiculo in jugador.vehiculos if vehiculo.k == 0]
        mov = 0
        result = Lancha()
        for barco in barcos:
            if barco.movimientos > mov:
                result = barco
                mov = barco.movimientos

        return result

    @staticmethod
    def _ataque_mas_utilizado(jugador):

        cant = 0
        result = AtaqueNormal()
        for ataque in jugador.arsenal.values():
            if ataque.totales > cant:
                result = ataque
                cant = ataque.totales

        return result

    def _ataque_mas_eficiente(self, jugador):
        maximo = 0
        result = AtaqueNormal()
        for item in self._porcentaje_por_barco(jugador):
            if item[1] > maximo:
                result = item[0]
        return result

    @staticmethod
    def _dano_por_barco(jugador):
        barcos = [vehiculo for vehiculo in jugador.vehiculos if vehiculo.k == 0]
        result = []
        for barco in barcos:
            try:
                ataque = barco.ataque_unico
                if ataque.exitoso:
                    result.append((barco.name, ataque.exitoso * ataque.damage))
                else:
                    result.append((barco.name, 0))
            except AttributeError:
                pass
        return result

    @staticmethod
    def _porcentaje_por_barco(jugador):

        normal = jugador.arsenal['AN']
        try:
            result = [('Ataque Normal', round((normal.exitoso / normal.totales) * 100))]
        except ZeroDivisionError:
            result = [('Ataque Normal', 0)]
        for barco in jugador.vehiculos:
            try:
                ataque = barco.ataque_unico
                result.append((barco.name, round((ataque.exitoso / ataque.totales) * 100)))
            except AttributeError:
                pass
            except ZeroDivisionError:
                result.append((barco.name, 0))
        return result

    @staticmethod
    def _porcentaje_exitosos(jugador):
        try:
            return round((jugador.ataques_exitosos / jugador.ataques_totales) * 100)
        except ZeroDivisionError:
            return 0

    def imprimir_stats(self):
        for jugador in [self.jugador1, self.jugador2]:
            print('######')
            print('Estadisticas del jugador: {}'.format(jugador))
            print('######')
            print('Porcentaje de ataques exitosos: {}%'.format(self._porcentaje_exitosos(jugador)))
            print('Porcentaje de ataques exitosos por barco y avion: ')
            for item in self._porcentaje_por_barco(jugador):
                print('    {}: {}%'.format(item[0], item[1]))
            print('Dano por barco: ')
            for item in self._dano_por_barco(jugador):
                print('    {}: {}'.format(item[0], item[1]))
            print('Dano total recibido: {}'.format(jugador.dano_total_recibido))
            print('Dano total causado: {}'.format(jugador.dano_total_causado))
            print('Ataque mas utilizado: {}'.format(self._ataque_mas_utilizado(jugador).name))
            print('Barco con mas movimientos: {}'.format(self._barco_con_mas_movimientos(jugador).name))
            print('Cantidad de turnos: {}'.format(jugador.turno))
            print('Ataque mas eficiente: {}'.format(self._ataque_mas_eficiente(jugador)))
