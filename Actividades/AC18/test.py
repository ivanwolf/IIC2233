import random
import simpy


class Proceso:
    def __init__(self, env):
        self.env = env
        self.accion = env.process(self.run())

    def run(self):
        # En el metodo run agregamos lo que ejecuta el proceso
        while True:
            yield self.env.timeout(1)  # El proceso retorna un evento
            print('tiempo actual = {0}'.format(self.env.now))


print(random.randint(0, 1))
