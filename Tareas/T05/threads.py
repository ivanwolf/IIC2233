from PyQt4 import QtCore, QtGui
import time, math, random
from evento import MoverPersonajeEvent, DisparoEvent


class Character(QtCore.QThread):
    trigger = QtCore.pyqtSignal(MoverPersonajeEvent)

    def __init__(self, parent, seq=None, x=460, y=360):
        super().__init__()
        self.padre = parent
        self.padre.pause_signal.connect(self.pausear)
        self.padre.endgame_signal.connect(self.terminar)

        self.secuencia = seq
        self.__position = (0, 0)
        self.position = (x, y)
        self.angulo = 0
        self.pasos = 0

        self.paused = False
        self.jugando = True

    def terminar(self):
        self.jugando = False

    def pixmap_siguiente(self):
        pixmap = self.secuencia.popleft()
        self.secuencia.append(pixmap)
        return pixmap

    def pausear(self):
        if self.paused:
            self.paused = False
        else:
            self.paused = True

    @property
    def pixmap_actual(self):
        return self.secuencia[0]

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value
        self.trigger.emit(MoverPersonajeEvent(
            self, self.x, self.y
        ))


class HeroeThread(Character):
    signal_revisar = QtCore.pyqtSignal()

    def __init__(self, parent, seq, proc):
        super().__init__(parent, seq)
        self.trigger.connect(parent.mover_heroe)
        self.signal_revisar.connect(proc.revisar_suministro)
        self.wait = 0.006

        self.direccion = (0, 0)
        self.shooting = 0
        self.moviendo = False

        self.score = 0
        self.hits = 0
        self.hp = 10
        self.municiones = 20

    def set_hp(self):
        if self.hp > 10:
            self.hp = 10

    def set_municiones(self):
        if self.municiones > 20:
            self.municiones = 20

    def run(self):
        time.sleep(self.wait)
        while self.jugando:
            time.sleep(self.wait)
            if not self.paused:
                antigua_pos = self.position
                direccion = rotar(self.angulo, self.direccion)
                self.position = (round(self.x + direccion[0], 6), round(self.y + direccion[1], 6))
                self.signal_revisar.emit()

                if antigua_pos != self.position:
                    self.moviendo = True
                else:
                    self.moviendo = False
        self.deleteLater()


class ZombieThread(Character):
    kill_signal = QtCore.pyqtSignal()
    init_signal = QtCore.pyqtSignal()
    signal_revisar = QtCore.pyqtSignal()
    signal_revisar_choques = QtCore.pyqtSignal(tuple)
    terminar = QtCore.pyqtSignal()

    def __init__(self, parent, seq, label, x, y, proc):
        super().__init__(parent, seq, x, y)
        self.label = label
        self.direccion = (1, 0)
        self.puede_avanzar = True
        self.colision = False
        self.muerto = False
        self.atacando = 0

        self.trigger.connect(parent.mover_zombie)
        self.terminar.connect(parent.borrar_thread)
        self.kill_signal.connect(parent.eliminar_zombie)
        self.signal_revisar.connect(proc.revisar_ataque)
        self.signal_revisar_choques.connect(proc.revisar_zombie)

        self.init_signal.connect(proc.init_zombie)
        self.init_signal.emit()

    def run(self):

        time.sleep(0.016)
        while not self.colision and self.jugando:
            time.sleep(0.016)
            if not self.paused:
                direccion = rotar(self.angulo, self.direccion)
                nueva_pos = round(self.x + direccion[0], 6), round(self.y + direccion[1], 6)
                self.signal_revisar_choques.emit(nueva_pos)
                if self.puede_avanzar:

                    self.position = nueva_pos
                    self.signal_revisar.emit()
                else:
                    a, b = 3 * random.randint(-1, 1), 3 * random.randint(-1, 1)
                    self.position = round(self.x + a * direccion[0], 6), \
                                    round(self.y + b * direccion[1], 6)
                    self.puede_avanzar = True

        self.kill_signal.emit()
        time.sleep(2)
        self.terminar.emit()
        self.deleteLater()


class Bala(QtCore.QThread):
    trigger = QtCore.pyqtSignal(DisparoEvent)
    terminar = QtCore.pyqtSignal()
    signal_revisar = QtCore.pyqtSignal()

    def __init__(self, parent, label, hero, proc):
        super().__init__()
        self.padre = parent
        self.label = label

        self.angulo = hero.angulo
        self.origen = hero.x + 40 * (.8 + math.cos(self.angulo)), hero.y + 40 * (.8 - math.sin(self.angulo))

        self.padre.pause_signal.connect(self.pausear)
        self.trigger.connect(parent.mover_bala)
        self.terminar.connect(parent.borrar_thread)
        self.signal_revisar.connect(proc.revisar_colision)

        self.__position = (0, 0)
        self.position = self.origen
        self.distancia_rec = 0

        self.paused = False
        self.colision = False

    def pausear(self):
        if self.paused:
            self.paused = False
        else:
            self.paused = True

    @property
    def position(self):
        return self.__position

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    @position.setter
    def position(self, value):
        self.__position = value
        self.trigger.emit(DisparoEvent(
            self.label, self.position[0], self.position[1]
        ))

    def run(self):
        time.sleep(0.001)
        while self.distancia_rec < 350 and not self.colision:
            time.sleep(0.001)
            if not self.paused:
                self.position = (round(self.position[0] + math.cos(self.angulo), 8),
                                 round(self.position[1] - math.sin(self.angulo), 8))
                self.distancia_rec += 1
                self.signal_revisar.emit()
        self.terminar.emit()
        self.deleteLater()


class Suministro(QtCore.QThread):
    terminar = QtCore.pyqtSignal()
    init_signal = QtCore.pyqtSignal()

    def __init__(self, parent, label, tipo, x, y, proc):
        super().__init__()
        self.label = label
        self.padre = parent
        self.tipo = tipo
        self.x = x
        self.y = y

        self.tomado = False
        self.paused = False

        self.padre.pause_signal.connect(self.pausear)
        self.terminar.connect(parent.borrar_thread)
        self.init_signal.connect(proc.init_sumin)
        self.init_signal.emit()

    def pausear(self):
        if self.paused:
            self.paused = False
        else:
            self.paused = True

    def run(self):
        i = 0
        while i < 60:
            time.sleep(0.5)
            if self.tomado:
                self.terminar.emit()
                return
            if not self.paused:
                i += 1

        self.terminar.emit()
        self.deleteLater()


class ZombieGenerator(QtCore.QThread):
    signal = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.padre = parent
        self.padre.pause_signal.connect(self.pausear)
        self.padre.endgame_signal.connect(self.terminar)
        self.padre.time_signal.connect(self.set_tasa)
        self.signal.connect(parent.crear_zombie)
        self.paused = False
        self.jugando = True
        self.tasa = 1.4

    def set_tasa(self):
        self.tasa += 0.09
        print(self.tasa)

    def terminar(self):
        self.jugando = False

    def pausear(self):
        if self.paused:
            self.paused = False
        else:
            self.paused = True

    def run(self):
        time.sleep(1)
        while self.jugando:
            time.sleep(round(random.expovariate(self.tasa), 4) + 0.5)
            if not self.paused:
                self.signal.emit()
        self.deleteLater()


class SuminGenerator(QtCore.QThread):
    signal = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.padre = parent
        self.padre.pause_signal.connect(self.pausear)
        self.padre.endgame_signal.connect(self.terminar)
        self.signal.connect(parent.crear_suministro)
        self.paused = False
        self.jugando = True

    def terminar(self):
        self.jugando = False

    def pausear(self):
        if self.paused:
            self.paused = False
        else:
            self.paused = True

    def run(self):
        while self.jugando:
            tiempo = round(random.randint(4, 6))
            i = 0
            while i < tiempo:
                time.sleep(0.01)
                if not self.paused:
                    time.sleep(1)
                    i += 1
            self.signal.emit()

        self.deleteLater()


class TimeCounter(QtCore.QThread):
    signal = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.padre = parent
        self.signal.connect(parent.actualizar_reloj)
        self.padre.pause_signal.connect(self.pausear)
        self.padre.endgame_signal.connect(self.terminar)

        self.paused = False
        self.jugando = True

    def terminar(self):
        self.jugando = False

    def pausear(self):
        if self.paused:
            self.paused = False
        else:
            self.paused = True

    def run(self):
        while self.jugando:
            time.sleep(0.001)
            if not self.paused:
                time.sleep(1.00)
                self.signal.emit()
        self.deleteLater()


def rotar(theta, vec):
    T = [[math.cos(theta), math.sin(theta)], [-math.sin(theta), math.cos(theta)]]
    return T[0][0] * vec[0] + T[0][1] * vec[1], T[1][0] * vec[0] + T[1][1] * vec[1]
