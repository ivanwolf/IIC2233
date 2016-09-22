class MoverPersonajeEvent:
    def __init__(self, personaje, x, y):
        self.personaje = personaje
        self.x = x
        self.y = y


class DisparoEvent:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y


class MuereZombieEvent:
    def __init__(self, zombie, bala):
        self.zombie = zombie
        self.bala = bala
