from banner import *


class Interfaz(Banner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def imprimir_cursos(lista_cursos):
        """
        Muestra en consola los cursos de la lista
        :param lista_cursos: Lista con objetos tipo Curso
        """
        if lista_cursos:
            for i in range(len(lista_cursos)):
                print('[{}]:'.format(i), lista_cursos[i], sep=' ')
                print('--------------------------------', '\n')
        else:
            print('No hay ramos por tomar')

    @staticmethod
    def imprimir_evaluaciones(lista_evaluaciones, path='data/calendario.txt'):
        """
        :param lista_evaluaciones: Lista con objetos del tipo Evaaluacion
        :param path: Direccion donde guardar el archivo .txt, por defecto se guara en data/calendario.txt
        :return: imprime el calendario en la consola y genera un archivo .txt
        """
        file = open(path, 'w+')
        file.write('Hello World \n')
        if lista_evaluaciones:
            for evaluacion in lista_evaluaciones:
                file.write(str(evaluacion) + '\n')
                print(evaluacion)

        file.close()

    @staticmethod
    def imprimir_horario(lista_cursos, path='data/horario.txt'):
        """
        Esquema sacado de stackoverflow.com/questions/7617925/ , PUEDE QUE HAYAN COINCIDENCIAS CON OTRAS TAREAS
        :param lista_cursos: Lista con objetos tipo cursos
        :param path: Direccion donde guardar el archivo .txt, por defecto se guara en data/horario.txt
        :return: imprime el horario en la consola y genera un archivo .txt
        """

        hline = ''
        for i in range(7):
            hline += '-------------||'
        headers = ['Modulo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado ']
        table = [['1', '', '', '', '', '', ''],
                 ['2', '', '', '', '', '', ''],
                 ['3', '', '', '', '', '', ''],
                 ['4', '', '', '', '', '', ''],
                 ['5', '', '', '', '', '', ''],
                 ['6', '', '', '', '', '', ''],
                 ['7', '', '', '', '', '', '']]

        for curso in lista_cursos:
            for tupla in curso.horario:
                table[tupla[0]][tupla[1]] = '{}-{}'.format(curso.sigla, curso.sec)
        if path:
            file = open(path, 'w+')
            file.write('Hello World \n')
            file.write(hline + '\n')
            file.write('||'.join(column.ljust(13) for column in headers) + '\n')
            file.write(hline + '\n')

        print('\n')
        print(hline)
        print('||'.join(column.ljust(13) for column in headers), )
        print(hline)

        for row in table:
            if path:
                file.write('||'.join(str(column).ljust(13) for column in row) + '\n', )
                file.write(hline + '\n')

            print('||'.join(str(column).ljust(13) for column in row), )
            print(hline)
        file.close()
        print('\n', '\n')

    def correr(self):
        """
        Corre la interfaz para que el usuario pueda interactuar todas las veces con la clase Bummer UC
        :return: True al salir del programa
        """
        print('Bienvenido a Bummer UC')
        print('y: Log In')
        click = input('q: Salir \n')
        if click == 'q':
            return True

        self.log_in()

        if isinstance(self.usuario_actual, Alumno):
            click = 1
            while click != '0':
                print('[1]: Inscribir curso',
                      '[2]: Botar curso',
                      '[3]: Generar horario',
                      '[4]: Generar calendario de ealuaciones',
                      '[5]: Mostrar informacion personal',
                      '[0]: Salir', sep=' \n')
                click = input('\n')

                if click == '1':
                    if self.cumple_horario(self.usuario_actual):
                        curso = self.buscar_curso(int(input('NRC: ')))
                        if curso:
                            self.inscribir_curso(self.usuario_actual, curso)
                    else:
                        print('Solo puedes tomar ramos durante tu periodo asignado \n')

                if click == '2':
                    if self.cumple_horario(self.usuario_actual):
                        self.imprimir_cursos(self.usuario_actual.cursos_por_tomar)
                        i = int(input('Seleccione el ramo: '))
                        curso = self.usuario_actual.cursos_por_tomar[i]
                        self.retirar_curso(self.usuario_actual, curso)
                    else:
                        print('Solo puedes retirar cursos durante tu periodo asignado \n')
                if click == '3':
                    self.imprimir_cursos(self.usuario_actual.cursos_por_tomar)
                    self.imprimir_horario(self.usuario_actual.cursos_por_tomar)

                if click == '4':
                    for curso in self.usuario_actual.cursos_por_tomar:
                        self.imprimir_evaluaciones(curso.evaluaciones)

                if click == '5':
                    print('Nombre: {}'.format(self.usuario_actual.nombre))
                    print('Grupo: {}'.format(self.usuario_actual.grupo))
                    print('Cursos por tomar: {}'.format(self.usuario_actual.cursos_por_tomar))
                    print('Permiso especial: {}'.format(self.usuario_actual.permiso))

                if click == 'q':
                    return True

        if isinstance(self.usuario_actual, Profesor):
            click = '5'
            while click != '0':
                print('[1]: Otorgar permiso especial',
                      '[2]: Quitar ermiso especial',
                      '[0]: Salir', sep=' \n')
                click = input('\n')

                if click == '1':
                    alumno = input('Nombre sel alumno: ')
                    sigla = input('Sigla del curso: ')
                    self.dar_permiso(alumno, sigla)

                if click == '2':
                    alumno = input('Nombre sel alumno: ')
                    sigla = input('Sigla del curso: ')
                    self.quitar_permiso(alumno, sigla)

                if click == 'q':
                    return True
        self.correr()
