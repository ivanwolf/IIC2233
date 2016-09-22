from ataque import MisildeCrucero, Napalm, MisilBalisico, AtaqueKamikaze, Paralizador, Ingenieros


class Vehiculo:
    """
    Una pieza que forma parte del juego
    """
    area_utilizada = None
    resistencia_inicial = None
    k = None

    def __init__(self):
        self.resistencia = self.resistencia_inicial
        self.posicion_cabeza = None

        self.napalm = False
        self.movimientos = 0

    @property
    def area(self):
        """ Retorna una lista con las tuplas que ocupa el vehiculo """
        area = self.area_utilizada
        return [(i, j, self.k) for i in range(area[0]) for j in range(area[1])]

    @property
    def ubicacion(self):
        """
        Retorna una lista con las posiciones que ocupa el vehiculo
        (es la posicion de la "cabeza" mas el area que ocupa)
        """
        if self.posicion_cabeza:
            pos = self.posicion_cabeza
            return [(pos[0] + q[0], pos[1] + q[1], self.k) for q in self.area]
        return self.area

    @property
    def movimientos_posibles(self):
        pos = self.posicion_cabeza
        return [(pos[0] + i, pos[1] + j, self.k) for i in (1, 0, -1) for j in (-1, 0, 1)]


class BarcoPequeno(Vehiculo):
    area_utilizada = (3, 1)
    resistencia_inicial = 30
    k = 0

    def __init__(self):
        super().__init__()
        self.ataque_unico = MisilBalisico()

    def __repr__(self):
        return 'BP'

    @property
    def name(self):
        return 'Barco Pequeno'


class BuquedeGuerra(Vehiculo):
    area_utilizada = (2, 3)
    resistencia_inicial = 60
    k = 0

    def __init__(self):
        super().__init__()
        self.ataque_unico = MisildeCrucero()

    def __repr__(self):
        return 'BG'

    @property
    def name(self):
        return 'Buque de Guerra'


class Lancha(Vehiculo):
    area_utilizada = (2, 1)
    resistencia_inicial = 1
    k = 0

    def __init__(self):
        super().__init__()
        self.ataque_unico = None

    def __repr__(self):
        return 'LA'

    @property
    def movimientos_posibles(self):
        return 'All'

    @property
    def name(self):
        return 'Lancha'


class Puerto(Vehiculo):
    area_utilizada = (4, 2)
    resistencia_inicial = 80
    k = 0

    def __init__(self):
        super().__init__()
        self.ataque_unico = Ingenieros()

    def __repr__(self):
        return 'PU'

    @property
    def movimientos_posibles(self):
        return None

    @property
    def name(self):
        return 'Puerto'


class AvionExplorador(Vehiculo):
    area_utilizada = (3, 3)
    k = 1

    def __init__(self):
        super().__init__()
        self.ataque_unico = Paralizador()
        self.turno_paralisis = 0

    def paralizado(self, n):
        if self.turno_paralisis == 0:
            return False, 0
        else:
            if n - self.turno_paralisis > 5:
                return False, 0
        return True, 5 - (n - self.turno_paralisis)

    def __repr__(self):
        return 'AE'

    @property
    def name(self):
        return 'Avion Explorador'


class Kamikaze(Vehiculo):
    area_utilizada = (1, 1)
    k = 1

    def __init__(self):
        super().__init__()
        self.ataque_unico = AtaqueKamikaze()

    def __repr__(self):
        return 'KZ'

    @property
    def name(self):
        return 'Kamikaze'


class AviondeCaza(Vehiculo):
    area_utilizada = (1, 1)
    k = 1

    def __init__(self):
        super().__init__()
        self.ataque_unico = Napalm()

    def __repr__(self):
        return 'AC'

    @property
    def name(self):
        return 'Avion de Caza'
