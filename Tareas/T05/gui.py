# -*- coding: UTF-8 -*-
import os, math, time, random
from PyQt4 import QtCore, QtGui, uic
from collections import deque
from threads import HeroeThread, Bala, ZombieThread, ZombieGenerator, Suministro, SuminGenerator, TimeCounter
from proc import Procesador

mainwindow_ui = uic.loadUiType('interfaz/mainwindow.ui')
gamewindow_ui = uic.loadUiType('interfaz/gamewindow.ui')
end_game_ui = uic.loadUiType('interfaz/end_game.ui')
new_game_ui = uic.loadUiType('interfaz/new_game.ui')


class Ventana(*new_game_ui):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.padre = parent
        self.pushButton.clicked.connect(self.button_clicked)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def button_clicked(self):
        self.padre.new_game()
        self.accept()


class Dialogo(*end_game_ui):
    def __init__(self, parent, score):
        super().__init__()
        self.setupUi(self)
        self.padre = parent
        self.buttonBox.accepted.connect(self.padre.new_game)
        self.buttonBox.rejected.connect(self.padre.salir)
        self.scoreLabel.setText('Puntaje final: {}'.format(score))
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)


class MainWindow(*mainwindow_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.show()
        self.ventana = Ventana(self)
        self.ventana.show()
        self.actionSalir.triggered.connect(self.salir)
        self.actionNewGame.triggered.connect(self.new_game)

    def keyPressEvent(self, QKeyEvent):
        self.centralWidget().keyPressEvent(QKeyEvent)

    def keyReleaseEvent(self, QkeyEvent):
        self.centralWidget().keyReleaseEvent(QkeyEvent)

    def salir(self):
        QtGui.qApp.quit()

    def mostrar_dialogo(self, n):
        self.dialogo = Dialogo(self, n)
        self.dialogo.show()

    def new_game(self):
        try:
            self.centralWidget().setParent(None)
            self.centralWidget().deleteLater()
        except AttributeError:
            pass
        finally:
            self.setCentralWidget(GameWindow(self))


class GameWindow(*gamewindow_ui):
    pause_signal = QtCore.pyqtSignal()
    endgame_signal = QtCore.pyqtSignal(int)
    time_signal = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.setup_pixmap()

        self.padre = parent
        self.endgame_signal.connect(self.padre.mostrar_dialogo)

        self.threads = []
        self.running = True
        self.juego_terminado = False

        self.xcursor = 0
        self.ycursor = 0
        self.tiempo = 0
        self.atacando = 0

        self.run()

    def run(self):

        self.proc = Procesador(self)

        self.crear_heroe()
        self.proc.hero = self.hero

        self.contador = TimeCounter(self)
        self.contador.start()

        self.hero.start()

        self.zombie_generator = ZombieGenerator(self)
        self.zombie_generator.start()

        self.suministro_generator = SuminGenerator(self)
        self.suministro_generator.start()

    def setup_pixmap(self):
        self.path = os.path.join(os.path.dirname(__file__), "interfaz/sprites/")

        self.seq_hero = deque()
        self.seq_hero.append(QtGui.QPixmap(self.path + 'hero_2.png').scaled(60, 60))
        self.seq_hero.append(QtGui.QPixmap(self.path + 'hero_1.png').scaled(60, 60))
        self.seq_hero.append(QtGui.QPixmap(self.path + 'hero_2.png').scaled(60, 60))
        self.seq_hero.append(QtGui.QPixmap(self.path + 'hero_3.png').scaled(60, 60))

        self.seq_zom = deque()
        self.seq_zom.append(QtGui.QPixmap(self.path + 'frame-1.png').scaled(40, 40))
        self.seq_zom.append(QtGui.QPixmap(self.path + 'frame-2.png').scaled(40, 40))

        self.hit_zom = QtGui.QPixmap(self.path + 'frame_hit-1.png').scaled(40, 40)

        self.blood_pixmap = []
        for i in range(7):
            pixmap = QtGui.QPixmap(self.path + 'bloodsplats_000{}.png'.format(i + 1)).scaled(40, 40)
            self.blood_pixmap.append(pixmap)

        self.hpbar_pixmap = []
        self.munibar_pixmap = []
        for i in range(11):
            h_pixmap = QtGui.QPixmap(self.path + 'VIDA_{}.png'.format(i))
            m_pixmap = QtGui.QPixmap(self.path + 'VIDA_{}_hit.png'.format(i))
            self.hpbar_pixmap.append(h_pixmap)
            self.munibar_pixmap.append(m_pixmap)

        self.hithpbar_pixmap = QtGui.QPixmap(self.path + 'VIDA_-1.png')
        self.bala_pixmap = QtGui.QPixmap(self.path + 'bullet.png').scaled(15, 15)
        self.medpack_pixmap = QtGui.QPixmap(self.path + 'medpack.png').scaled(40, 40)
        self.municiones_pixmap = QtGui.QPixmap(self.path + 'municiones.png').scaled(40, 40)

        background = QtGui.QPixmap(self.path + 'grasses.gif')
        health_bar = QtGui.QPixmap(self.path + 'VIDA_10.png')
        muni_bar = QtGui.QPixmap(self.path + 'VIDA_10_hit.png')

        self.backgroundLabel.setPixmap(background)
        self.healthLabel.setPixmap(health_bar)
        self.muniLabel.setPixmap(muni_bar)

    def crear_heroe(self):
        self.heroLabel.setPixmap(self.seq_hero[0])
        self.heroLabel.show()
        self.hero = HeroeThread(self, self.seq_hero, self.proc)

    def crear_zombie(self):

        x, y = random.randint(0, 1000), random.randint(0, 700)
        x, y = random.choice([(0, y), (940, y), (x, 0), (x, 640)])

        label = QtGui.QLabel(self)
        label.setGeometry(x, y, 60, 60)
        label.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        label.show()

        zombie = ZombieThread(self, self.seq_zom, label, x, y, self.proc)
        zombie.start()
        self.threads.append(zombie)

    def crear_bala(self):

        label = QtGui.QLabel(self)
        label.setGeometry(0, 0, 20, 20)
        pixmap = self.bala_pixmap.transformed(QtGui.QTransform().rotate(90 - self.hero.angulo * 180 / math.pi))
        label.setPixmap(pixmap)
        label.show()

        disparo = Bala(self, label, self.hero, self.proc)
        disparo.start()
        self.threads.append(disparo)

    def crear_suministro(self):
        x, y = random.randint(0, 960), random.randint(0, 660)
        label = QtGui.QLabel(self)
        label.setGeometry(x, y, 40, 40)
        if random.randint(0, 20) < 5:
            pixmap = self.medpack_pixmap
            tipo = 'medpack'
        else:
            pixmap = self.municiones_pixmap
            tipo = 'municiones'
        label.setPixmap(pixmap)
        label.show()

        suministro = Suministro(self, label, tipo, x, y, self.proc)
        suministro.start()
        self.threads.append(suministro)

    def mouseMoveEvent(self, QMouseEvent):
        if not self.juego_terminado and self.running:
            self.xcursor, self.ycursor = QMouseEvent.x(), QMouseEvent.y()

    def mousePressEvent(self, QmouseEvent):
        if not self.juego_terminado and self.running:
            self._disparar()
            time.sleep(0.01)

    def mouseReleaseEvent(self, QmouseEvent):
        if not self.juego_terminado and self.running:
            time.sleep(0.04)

    def keyPressEvent(self, QKeyEvent):
        if not self.juego_terminado:
            if QKeyEvent.key() == QtCore.Qt.Key_Space:
                self.pausear()
            elif QKeyEvent.key() == QtCore.Qt.Key_A:
                self.hero.direccion = (0, -1)
            elif QKeyEvent.key() == QtCore.Qt.Key_D:
                self.hero.direccion = (0, 1)
            elif QKeyEvent.key() == QtCore.Qt.Key_W:
                self.hero.direccion = (1, 0)
            elif QKeyEvent.key() == QtCore.Qt.Key_S:
                self.hero.direccion = (-1, 0)

    def keyReleaseEvent(self, QkeyEvent):
        self.hero.direccion = (0, 0)

    def mover_heroe(self, MoverPersonajeEvent):
        personaje = MoverPersonajeEvent.personaje
        pixmap = personaje.pixmap_actual

        if 0 < personaje.shooting and personaje.shooting < 30:
            pixmap = QtGui.QPixmap(self.path + 'hero_4.png').scaled(60, 60)
            personaje.shooting += 1

        elif personaje.moviendo:
            if personaje.pasos > 20:
                pixmap = personaje.pixmap_siguiente()
                personaje.pasos = 0
            else:
                pixmap = personaje.pixmap_actual
            personaje.shooting = 0

        try:
            pixmap = pixmap.transformed(QtGui.QTransform().rotate(90 - personaje.angulo * 180 / math.pi))
            self._calcular_hero_angulo()
        except AttributeError:
            pass

        self.heroLabel.setPixmap(pixmap)
        self.heroLabel.move(MoverPersonajeEvent.x, MoverPersonajeEvent.y)
        personaje.pasos += 1

    def mover_bala(self, DisparoEvent):
        label = DisparoEvent.image
        label.move(DisparoEvent.x, DisparoEvent.y)

    def mover_zombie(self, MoverPersonajeEvent):
        zombie = MoverPersonajeEvent.personaje
        if 0 < zombie.atacando and zombie.atacando < 50:
            pixmap = self.hit_zom
            zombie.atacando += 1

        else:
            if zombie.pasos > 20:
                pixmap = zombie.pixmap_siguiente()
                zombie.pasos = 0
            else:
                pixmap = zombie.pixmap_actual

            zombie.atacando = 0

        self._calcular_zombie_angulo(zombie)

        zombie.label.setPixmap(pixmap)
        zombie.label.move(MoverPersonajeEvent.x, MoverPersonajeEvent.y)
        zombie.pasos += 1

    def actualizar_reloj(self):
        segundos = str(self.tiempo % 60).zfill(2)
        minutos = str(self.tiempo // 60).zfill(2)
        self.timeLabel.setText('{0}:{1}'.format(minutos, segundos))
        if self.tiempo % 10 == 0:
            self.time_signal.emit()

        self.tiempo += 1

    def actualizar_score(self):
        self.hero.score += self.hero.hits + round(self.tiempo / 2)
        self.scoreLabel.setText('{}'.format(str(self.hero.score)))

    def actualizar_sumin(self):
        if not self.juego_terminado:
            hp = self.hero.hp
            m = self.hero.municiones
            n = int(math.ceil(self.hero.municiones) / 2)

            self.healthLabel.setPixmap(self.hpbar_pixmap[hp])
            self.muniLabel.setPixmap(self.munibar_pixmap[n])

            self.strhpLabel.setText(str(hp) + '/10')
            self.munistrLabel.setText(str(m) + '/20')

    def _calcular_hero_angulo(self):
        x, y = self.hero.x + 35, self.hero.y + 35
        angulo = math.atan2(y - self.ycursor, self.xcursor - x)
        if angulo < 0:
            angulo += 2 * math.pi
        self.hero.angulo = angulo

    def _calcular_zombie_angulo(self, zombie):
        heroe = self.hero
        xhero, yhero = heroe.x + 35, heroe.y + 35
        x, y = zombie.x + 30, zombie.y + 30
        angulo = math.atan2(y - yhero, xhero - x)
        if angulo < 0:
            angulo += 2 * math.pi
        zombie.angulo = angulo

    def _disparar(self):
        self.hero.shooting = 1
        if self.hero.municiones:
            self.hero.municiones -= 1
            self.crear_bala()
            self.actualizar_sumin()

    def borrar_thread(self):
        thread = self.sender()
        thread.label.setParent(None)
        self.threads.remove(thread)

    def pausear(self):
        if self.running:
            self.pauseLabel.setText('Pausa')
            self.running = False
        else:
            self.pauseLabel.setText('')
            self.running = True

        self.pause_signal.emit()

    def eliminar_zombie(self):
        zombie = self.sender()
        pixmap = random.choice(self.blood_pixmap)
        zombie.label.setPixmap(pixmap)
        zombie.muerto = True

    def end_game(self):
        self.actualizar_sumin()
        self.juego_terminado = True
        self.endgame_signal.emit(self.hero.score)
