class Curso:
    def __init__(self, dic, lista_requisitos, lista_evaluaciones):
        self.nombre = dic['curso']
        self.sigla = dic['sigla']
        self.profesor = dic['profesor']
        self.sec = dic['sec']
        self.nrc = dic['NRC']
        self.campus = dic['campus']
        self.ofrecidos = dic['ofr']
        self.creditos = dic['cred']
        self.lista_alumnos = []
        self.horario = Horario(dic).horarios
        self.requisitos = []
        self.agregar_requisitos(lista_requisitos)
        self.evaluaciones = []
        self.agregar_evaluaciones(lista_evaluaciones)

    def __repr__(self):
        return self.sigla

    @property
    def disponibles(self):
        return self.ofrecidos - len(self.lista_alumnos)

    def agregar_requisitos(self, lista_requisitos):
        """
        Busca si es que el curso tiene requisitos y de ser asi retorna una lista con las siglas
        :param lista_requisitos: lista de diccionarios que representan todos los requisitos
        :return: objeto del tipo lista donde cada item tiene una lista
        """
        string = ''
        for dic in lista_requisitos:
            if self.sigla == dic['sigla']:
                string = dic['prerreq']

        if string:
            l = string.split(' o ')
            for i in range(len(l)):
                l[i] = l[i].replace('(c)', '').strip(')').strip('(')
                l[i] = l[i].split(' y ')
            self.requisitos = l
        else:
            self.requisitos = []

    def agregar_evaluaciones(self, lista_evaluaciones):

        for dic in lista_evaluaciones:
            if self.sigla == dic['sigla']:
                self.evaluaciones.append(Evaluacion(dic))


class Horario:
    def __init__(self, dic):
        """
        Crea el objeto tipo Horario a partir de un diccionario que corresponde a algun curso
        :param dic: objeto tipo diccionario
        """
        self.curso = dic['curso']
        self.horarios = []
        self.agregar_horarios(dic)

    def __repr__(self):
        return 'Catedra: {}, Ayudantia: {}, Laboratorio: {}'.format(self.hora_cat, self.hora_ayud, self.hora_lab)

    def agregar_horarios(self, dic):
        if 'hora_cat' in dic.keys():
            self.horarios += self.str_to_modulo(dic['hora_cat'])
        if 'hora_ayud' in dic.keys():
            self.horarios += self.str_to_modulo(dic['hora_ayud'])
        if 'hora_clab' in dic.keys():
            self.horarios += self.str_to_modulo(dic['hora_lab'])
        if 'hora_terr' in dic.keys():
            self.horarios += self.str_to_modulo(dic['hora_terr'])

    @staticmethod
    def str_to_modulo(string):
        """
        Transforma un str de la forma "L-W-V:4" en una liste de tuplas (x,y) donde 'x' representa el modulo de clases,
        y la variable 'y' representa el dia de la semana segun el dicionario
        :param string: objeto tipo string
        :return: lista con objetos tipo tupla
        """
        lista = []
        dic = {'L': 1, 'M': 2, 'W': 3, 'J': 4, 'V': 5, 'S': 6}
        l = string.split(':')
        dias = l[0].split('-')
        modulos = l[1].split(',')

        for dia in dias:
            for modulo in modulos:
                lista.append((int(modulo)-1, dic[dia]))
        return lista


class Evaluacion:
    def __init__(self, dic):
        self.curso = dic['sigla']
        self.fecha = dic['fecha']
        self.tipo = dic['tipo']

    def __repr__(self):
        return 'Curso: {}-{} Fecha: {}'.format(self.curso, self.tipo, self.fecha)
