__author__ = 'ivanwolf'


class MetaRobot(type):

    def __new__(cls, nombre, base_clases, diccionario):
        if not nombre == 'Robot':
            raise NameError('Solo la clase robot puede usar esta metaclase')
        diccionario.update(dict({'creador': 'ivanwolf15', 'ip_inicio': '190.102.62.283'}))
        diccionario.update(dict({'check_creator': check_creator, 'cortar_conexion': cortar_conexion}))
        diccionario.update(dict({'cambiar_nodo': cambiar_nodo}))

        return super().__new__(cls, nombre, base_clases, diccionario)



def check_creator(self):
    if self.creador not in self.creadores:
        print('El creador NO se encuentra en la lista de programadores')
    else:
        print('El creador SI se encuentra en la lista')

def cortar_conexion(self):
    if self.Verificar():
        print('Se encunetra un hacker en este puerto!')
        self.actual.hacker = 0
        print('El hacker se envio al puerto 0')

def cambiar_nodo(self, nuevo):
    print('Puerto actual: {0}'.format(self.actual.ide))
    self.actual = nuevo
    print('Nos trasladamos al puerto {0}'.format(nuevo.ide))
