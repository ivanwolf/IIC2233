from collections import deque
from random import uniform, random, expovariate


class Jugador:
    n = 1

    def __init__(self):
        self.ide = self.n
        self.habilidad = uniform(1, 10)
        self.partidos_jugados = 0
        Jugador.n += 1

    def __repr__(self):
        return 'Jugador: {0}'.format(self.ide)

    def se_retira(self):
        if random() <= 0.25 + self.partidos_jugados * 0.05:
            return True
        return False


class Partida:
    def __init__(self, jugador_uno, jugador_dos):
        self.jugador_actual = jugador_uno
        self.contrincante = jugador_dos

        self.ganador = None
        self.perdedor = None
        self.duracion = round(uniform(4, 6))

    def definir_ganador(self):
        total = self.jugador_actual.habilidad + self.contrincante.habilidad
        if random() <= self.jugador_actual.habilidad / total:
            self.ganador = self.jugador_actual
            self.perdedor = self.contrincante
        else:
            self.ganador = self.contrincante
            self.perdedor = self.jugador_actual
        print('[FIN DE A PARTIDA] El gandor fue el jugador {0}'.format(self.ganador.ide))


class Simulacion:
    def __init__(self, tiempo_maximo, tasa_llegada):
        self.tiempo_max_sim = tiempo_maximo
        self.tasa_de_llegada = tasa_llegada

        self.partida = Partida(Jugador(), Jugador())
        self.cola_espera = deque()
        self.cola_espera.append(Jugador())

        self.tiempo_simulacion = 0
        self.tiempo_prox_partida = 0
        self.tiempo_prox_jugador = 0

    def proximo_jugador(self):
        self.tiempo_prox_jugador = self.tiempo_simulacion + round(expovariate(self.tasa_de_llegada) + 0.5)

    def fin_partida(self):
        self.tiempo_prox_partida = self.tiempo_simulacion + self.partida.duracion

    def run(self):

        self.proximo_jugador()
        self.fin_partida()

        while self.tiempo_simulacion < self.tiempo_max_sim:

            if self.tiempo_prox_jugador < self.tiempo_prox_partida:
                self.tiempo_simulacion = self.tiempo_prox_jugador

            else:
                self.tiempo_simulacion = self.tiempo_prox_partida
            print('Tiempo: {0}'.format(self.tiempo_simulacion))

            if self.tiempo_simulacion == self.tiempo_prox_jugador:
                jugador = Jugador()
                self.cola_espera.append(jugador)
                print('[COLA] Acaba de llegar el jugador {0}, se ha puesto en la fila'.format(jugador.ide))

                self.proximo_jugador()


            else:

                self.partida.definir_ganador()

                if self.partida.perdedor.se_retira():
                    print('El jugador {0} ha decido retirarse'.format(self.partida.perdedor.ide))
                else:
                    self.cola_espera.append(self.partida.perdedor)

                try:
                    jugador_nuevo = self.cola_espera.popleft()
                    self.partida = Partida(self.partida.ganador, jugador_nuevo)
                except IndexError:
                    print('Ya no quedan mas jugadores')
                    return True

                self.fin_partida()

if __name__ == '__main__':
    tasa = 1 / 15
    tiempo_max = 70
    s = Simulacion(tiempo_max, tasa)
    s.run()
