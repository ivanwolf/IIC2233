import random
import simpy

SIM_TIME = 500
INTERVAL = 10
TABLES = 3
NAME = "Cliente {0}"


def paciencia(cliente):
    return 2 * cliente.priority + 7


class Cliente():
    def __init__(self, *args, **kwargs):
        self.priority = kwargs['priority']
        self.name = kwargs['name']
        self.arrive = kwargs['arrive']
        self.number = kwargs['arrival_number']
        self.exit = None


class Restaurante():
    def __init__(self, env, capacity):
        self.env = env
        self.mesas = simpy.PriorityResource(env, capacity=capacity)
        self.__clientes = []
        self.n_atendidos = 1

    def espera(self, cliente):
        """
        ToDo
        """
        with self.mesas.request(priority=cliente.priority) as req:
            print('El Cliente {} llego al restaurant y tiene una prioridad {}'.format(
                cliente.name, cliente.priority
            ))
            yield req
            ## Vemos si es que lo llaman
            if random.randint(0, 9) == 1:
                print('Han llamado l cliente {}, no se sentara'.format(cliente.name))

            else:
                print('El cliente se sienta en la mesa')
                yield self.env.timeout(random.randint(30, 40))


def generador_clientes(env, lambdat, res):
    count = 0
    while True:
        yield env.timeout(random.expovariate(1 / lambdat))
        priority = random.randint(0, 25)
        cliente = Cliente(name=NAME.format(
            count), priority=priority, arrive=int(env.now), arrival_number=count)
        print("{0} ha arrivado al restaurant al instante {1} y \
                es el cliente numero {2}  del dia".format
            (
            cliente.name,
            env.now,
            count
        ))
        count += 1
        env.process(res.espera(cliente))


if __name__ == '__main__':
    env = simpy.Environment()
    restaurant = Restaurante(env, TABLES)
    pass