import random
from modulo import Tablero, Radar
from inteligencia import mejor_opcion, recursion
from vehiculo import Lancha, BuquedeGuerra, BarcoPequeno, Puerto, Kamikaze, AvionExplorador
from ataque import Napalm, AtaqueKamikaze


class Jugador:
    def __init__(self, nombre=None, n=0):
        self.name = nombre
        self.tablero = Tablero(jugador=self, largo=n)
        self.radar = Radar(jugador=self, largo=n)

        self.vehiculos = []
        self.arsenal = {}
        self.historial = []
        self.lista_radares = []
        self.oponente = None
        self.turno = 0

        self.dano_total_recibido = 0
        self.dano_total_causado = 0

        self.ataques_totales = 0
        self.ataques_exitosos = 0

        self.revelar = None
        self.nota = None
        self.movimineto = None

    def __repr__(self):
        return self.name

    @property
    def defeated(self):
        piezas = self.tablero.piezas
        if not piezas:
            return True
        if all([pieza.k for pieza in piezas]):
            return True

        return False

    def atacar(self, ataque, pos):

        n = self.turno
        tablero = self.tablero
        radar = self.radar
        oponente = self.oponente

        vehiculo_atacado = oponente.tablero[pos]
        rep = 'Turno {}: Ataque: {}, Pos: {}, Estado: '.format(n, ataque.name, pos)

        if vehiculo_atacado is None:
            print('Ataque fallido \n')
            rep += 'Fallido'
            radar.marcar('X', pos)

        else:
            if isinstance(self, Jugador):
                print('Ataque exitoso! Hemos encontrado algo en la posicion: {0}, {1}'.format(pos[0], pos[1]))
            rep += 'Exitoso'
            radar.marcar('O', pos)
            self.dano_total_causado += ataque.damage
            vehiculo_atacado.resistencia -= ataque.damage
            oponente.dano_total_recibido += ataque.damage
            ataque.exitoso += 1
            self.ataques_exitosos += 1

            if isinstance(ataque, Napalm):
                vehiculo_atacado.napalm = True

            elif isinstance(ataque, AtaqueKamikaze):
                for pieza in tablero.piezas:
                    if isinstance(pieza, Kamikaze):
                        pieza.resistencia = 0

        self.historial.append(rep)
        ataque.ultima_vez = n
        ataque.totales += 1
        self.ataques_totales += 1

    def explorar(self, pos):
        avion = None
        for vehiculo in self.tablero.piezas:
            if isinstance(vehiculo, AvionExplorador):
                avion = vehiculo

        try:
            paralizado = avion.paralizado(self.turno)
            encontrado = False

            if not paralizado[0]:
                print('Explorando ... ')
                for p in [(pos[0] + i, pos[1] + j, 0) for i in (1, 0, -1) for j in (-1, 0, 1)]:
                    try:
                        if self.oponente.tablero[p] is not None:
                            encontrado = True

                    except IndexError:
                        pass

                if encontrado:
                    print('Hemos encontrado algo al rededor del punto {}'.format(pos))
                    self.radar.marcar('E', pos)
                    if random.randint(0, 1):
                        self.oponente.revelar = random.choice(avion.ubicacion)
                        print('Hemos revelado donde esta nuestro avion explorador!')
                else:
                    print('No hemos encontrado nada')
                    self.radar.marcar('N', pos)

                    # avion.turno_paralisis = self.turno
            else:
                print('El avion esta paralizado, volvera a estar disponible en {} turnos'.format(paralizado[1]))
                raise PermissionError
        except AttributeError:
            print('No tenemos avion explorador!')

    def usar_ingenieros(self, ataque, vehiculo):
        vehiculo.resistencia += 1
        print('{} reparado exitosamente'.format(vehiculo.name))
        rep = 'Turno {}: Ingenieros --> {}'.format(self.turno, vehiculo.name)
        self.historial.append(rep)
        ataque.ultima_vez = self.turno
        ataque.totales += 1

    def usar_paralizador(self, ataque, pos1, pos2):

        tablero = self.oponente.tablero
        rep = 'Turno {}: Ataque: {}, Pos: {}y{}, Estado: '.format(self.turno, ataque.name, pos1, pos2)

        if tablero[pos1] is not None and tablero[pos2] is not None:
            avion = tablero[pos1]
            avion.turno_paralisis = self.turno
            print('Hemos paralizado al avion explorador enemigo!')
            rep += 'Exitoso'
            ataque.exitoso += 1
            self.ataques_exitosos += 1
        else:
            print('Ataque fallido')
            rep += 'Fallido'

        self.historial.append(rep)
        ataque.ultima_vez = self.turno
        ataque.totales += 1
        self.ataques_totales += 1

    def usar_misil_de_crucero(self, ataque, pos):
        oponente = self.oponente
        n = self.turno
        matches = 0
        pos_atacadas = []
        rep = 'Turno {}: Ataque: {}, Pos: {}, Estado: '.format(n, ataque.name, pos)

        if pos[0] == 'c':
            pos_atacadas = [(pos[1], i, 0) for i in range(self.tablero.largo)]
        if pos[0] == 'f':
            pos_atacadas = [(i, pos[1], 0) for i in range(self.tablero.largo)]

        for p in pos_atacadas:
            vehiculo_atacado = oponente.tablero[p]
            if vehiculo_atacado is not None:
                self.dano_total_causado += ataque.damage
                vehiculo_atacado.resistencia -= ataque.damage
                oponente.dano_total_recibido += ataque.damage
                ataque.exitoso += 1
                self.ataques_exitosos += 1
                matches += 1
        if matches:
            print('Ataue exitoso! Alcanzamos a {} posiciones!'.format(matches))
            rep += 'Exitoso'
        else:
            print('Ataque fallido')
            rep += 'Fallido'

        self.historial.append(rep)
        ataque.ultima_vez = n
        ataque.totales += 1
        self.ataques_totales += 1


class Computador(Jugador):
    def __init__(self, *args):
        super().__init__(*args)
        self.barcos = [Lancha(), BuquedeGuerra(), BarcoPequeno(), Puerto()]
        self.ultimo_ataque = tuple
        self.buena_idea = []

    def pensar(self):
        """
        La idea es buscar la posicion donde sea mas probable encontrar un barco, considerando los ataques exitosos y
        los fallidos
        :return: tuple (x,y,z)
        """

        if self.turno <= 10:
            largo = self.tablero.largo
            print('Ataque random')
            pos = (random.randint(0, largo - 1), random.randint(0, largo - 1))
            while self.radar[pos] in ['X', 'U', 'O']:
                pos = (random.randint(0, largo - 1), random.randint(0, largo - 1))
            return pos[0], pos[1], 0

        print('pensando ...')
        radar = self.radar

        db = [[0 for _ in range(radar.largo)] for _ in range(radar.largo)]
        hojas = []
        for barco in self.barcos:
            aux = self.barcos.copy()
            aux.remove(barco)
            hojas += recursion(barco, [radar], aux, db, radar)

        pos = mejor_opcion(db)
        print('pensando ...')
        return pos[0], pos[1], 0

    def podar(self):

        if self.nota is not None:
            vehiculo = self.nota
            for barco in self.barcos:
                if isinstance(barco, vehiculo.__class__):
                    self.barcos.remove(barco)
                    print('Ya no buscaremos {}'.format(barco.name))
            self.nota = None

    def primer_movimiento(self):
        if self.turno <= 3:
            largo = self.tablero.largo
            pos = (random.randint(1, largo - 2), random.randint(1, largo - 2))
            try:
                self.explorar(pos)
            except PermissionError:
                return False

            if self.radar[pos] == 'N':
                for (x, y) in [(pos[0] + i, pos[1] + j) for i in (1, 0, -1) for j in (-1, 0, 1)]:
                    self.radar.marcar('X', (x, y))

            return True
        return False
