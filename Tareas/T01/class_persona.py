class Persona:
    def __init__(self, dic):
        self.nombre = dic['nombre']
        self.usuario = dic['usuario']
        self.clave = dic['clave']

    def __repr__(self):
        return '{}'.format(self.nombre)


class Profesor(Persona):
    def __init__(self, dic):
        super().__init__(dic)


class Alumno(Persona):
    def __init__(self, dic):
        super().__init__(dic)
        self.grupo = 0
        self.cursos_aprobados = dic['ramos_pre']
        self.cursos_por_tomar = []
        self.idolos = dic['idolos']
        self.bacanosidad = dic['bacanosidad']
        self.permiso = 'Ninguno'

    @property
    def creditos_maximos(self):
        return 55 + (6 - int(self.grupo)) * 2

    @property
    def creditos_inscritos(self):
        suma = 0
        for curso in self.cursos_por_tomar:
            suma += curso.creditos
        return suma
