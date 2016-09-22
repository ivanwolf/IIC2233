class Ataque:
    area_atacada = (0, 0)
    damage = None
    disponibilidad = int()

    def __init__(self):

        self.totales = 0
        self.exitoso = 0
        self.ultima_vez = 0

    def disponible(self, n):
        """
        Revisa si es que el ataque esta diponible en el turno n
        :param n: int
        :return: (Bool, int) donde el entero representa en cuantos turnos mas estara disponible
        """
        if self.disponibilidad == 'Siempre' or self.ultima_vez == 0:
            return True, 0

        if (n - self.ultima_vez) >= self.disponibilidad:
            return True, 0

        return False, self.disponibilidad - (n - self.ultima_vez)


class AtaqueNormal(Ataque):
    area_atacada = (1, 1)
    damage = 10
    disponibilidad = 'Siempre'

    def __repr__(self):
        return 'AN'

    @property
    def name(self):
        return 'Ataque Normal'


class MisildeCrucero(Ataque):
    area_atacada = (1, 15)
    damage = 6
    disponibilidad = 3

    def __repr__(self):
        return 'MC'

    @property
    def name(self):
        return 'Misil de Crucero'


class Napalm(Ataque):
    area_atacada = (1, 1)
    damage = 10
    disponibilidad = 8

    def __repr__(self):
        return 'NA'

    @property
    def name(self):
        return 'Napalm'


class MisilBalisico(Ataque):
    area_atacada = (1, 1)
    damage = 20
    disponibilidad = 3

    def __repr__(self):
        return 'MB'

    @property
    def name(self):
        return 'Misil Balistico'


class AtaqueKamikaze(Ataque):
    area_atacada = (1, 1)
    damage = 10000000
    disponibilidad = 'Una vez'

    def __repr__(self):
        return 'AK'

    @property
    def name(self):
        return 'Ataque Kamikaze'


class Ingenieros(Ataque):
    area_atacada = (1, 1)
    damage = 0
    disponibilidad = 2

    def __repr__(self):
        return 'IN'

    @property
    def name(self):
        return 'Ingenieros'


class Paralizador(Ataque):
    area_atacada = (1, 1)
    damage = 0
    disponibilidad = 'Siempre'

    def __repr__(self):
        return 'PA'

    @property
    def name(self):
        return 'Paralizador'
