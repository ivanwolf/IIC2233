from PyQt4 import QtCore


class Procesador(QtCore.QThread):
    score_signal = QtCore.pyqtSignal()
    sumin_signal = QtCore.pyqtSignal()
    end_game_signal = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.padre = parent
        self.hero = None

        self.score_signal.connect(self.padre.actualizar_score)
        self.sumin_signal.connect(self.padre.actualizar_sumin)
        self.end_game_signal.connect(self.padre.end_game)

        self.lista_zombies = []
        self.lista_suministros = []

    def init_zombie(self):
        self.lista_zombies.append(self.sender())

    def init_sumin(self):
        self.lista_suministros.append(self.sender())

    def revisar_colision(self):
        bala = self.sender()
        i, j = bala.x + 10, bala.y + 10
        for zombie in self.lista_zombies.copy():
            x, y = zombie.x, zombie.y
            if x < i and i < x + 60 and y < j and j < y + 60 and not zombie.muerto:
                zombie.colision = True
                bala.colision = True
                self.hero.hits += 1
                self.lista_zombies.remove(zombie)
                self.score_signal.emit()
                return

    def revisar_suministro(self):
        hero = self.sender()
        i, j = hero.x + 30, hero.y + 30
        for suministro in self.lista_suministros.copy():

            x, y = suministro.x, suministro.y
            if x < i and i < x + 40 and y < j and j < y + 40:

                suministro.tomado = True
                if suministro.tipo == 'medpack':
                    hero.hp += 1
                    hero.set_hp()

                elif suministro.tipo == 'municiones':
                    hero.municiones += 6
                    hero.set_municiones()

                self.lista_suministros.remove(suministro)
                self.sumin_signal.emit()

    def revisar_ataque(self):
        zombie = self.sender()
        hero = self.hero
        i, j = zombie.x, zombie.y
        x, y = hero.x, hero.y

        if x < i and i < x + 60 and y < j and j < y + 60:
            if not zombie.atacando:
                zombie.atacando = 1
                hero.hp -= 1
                self.sumin_signal.emit()
                if hero.hp == 0:
                    self.end_game_signal.emit()

    def revisar_zombie(self, nueva_pos):
        zombie = self.sender()
        i, j = nueva_pos[0] + 20, nueva_pos[1] + 20
        k, l = nueva_pos[0] + 40, nueva_pos[1] + 40
        for cuerpo in self.lista_zombies:
            x, y = cuerpo.x, cuerpo.y
            if cuerpo != zombie and not cuerpo.muerto:
                if x < i and i < x + 60 and y < j and j < y + 60 or (
                                        x < k and k < x + 60 and y < l and l < y + 60):
                    zombie.puede_avanzar = False
                    return
