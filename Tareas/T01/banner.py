from class_curso import Curso
from class_persona import Profesor
from class_persona import Alumno
from bacanosidad import generar_lista_alumnos
from bacanosidad import generar_matriz
from bacanosidad import page_rank
from bacanosidad import agregar_bacanosidad
from bacanosidad import bacanosidad_min


class Banner:
    def __init__(self, usuario=None):
        self.usuario_actual = usuario  # Guarda el usuario actual del sistema puede ser un alumno o profesor
        self.lista_usuarios = []
        self.cursos = []
        self.personas = []
        self.time = None

    def instanciar_personas(self, diccionarios_personas):
        click = input('Guardar bacanosidad? (y/n) \n')
        if click == 'y':
            file = open('data/bacanosidad.txt', 'w+')

        diccionario_alumnos = generar_lista_alumnos(diccionarios_personas)
        A = generar_matriz(diccionario_alumnos)
        x = page_rank(A)
        agregar_bacanosidad(diccionario_alumnos, x)

        for dic in diccionarios_personas:
            if dic['alumno'] == 'SI':
                alumno = Alumno(dic)
                self.personas.append(alumno)
                alumno.grupo = self.calcular_grupo(alumno.bacanosidad, x)
                if click == 'y':
                    file.write('{}          {}\n'.format(alumno.nombre, alumno.bacanosidad))

            else:
                self.personas.append(Profesor(dic))
        print('Personas instanciadas correctamente')
        if click == 'y':
            file.close()
        return True

    def instanciar_cursos(self, diccionarios_curos, diccionarios_requisitos, diccionarios_evaluacion):
        """
        Crea todos los objetos de la clase Curso y los guarda como una lista en el atributo cursos
        :param diccionarios_curos: Lista de diccionarios sacados de cursos.txt
        :param diccionarios_requisitos: Lista de diccionarios sacados de requisitos.txt
        :param diccionarios_evaluacion: Lista de diccionarios sacados de evaluaciones.txt
        :return: Print al final de la funcion
        """

        for dic in diccionarios_curos:
            self.cursos.append(Curso(dic, diccionarios_requisitos, diccionarios_evaluacion))
        print('Cursos instanciados correctamente')
        return True

    def set_time(self):
        time = input('¿Que hora es? (hh:mm, reloj de 24 horas) \n')
        self.time = time

    def cumple_horario(self, alumno):
        g = alumno.grupo
        t = self.time
        return t >= '{}:30'.format(str(g+7).zfill(2)) and t <= '{}:30'.format(str(g+9).zfill(2))

    def log_in(self):
        """
        Se le pide al ususario que ingrese su ususario y cave, si coinciden entonces de cambia el parametro de la clase
        Banner, ususario_Actual
        :return: Boolean
        """
        usuario = input('Usuario: ')
        clave = input('Clave: ')

        for persona in self.personas:
            if persona.usuario == usuario:
                if persona.clave == clave:
                    self.usuario_actual = persona
                    print('Logeado correctamente como {} \n'.format(type(self.usuario_actual).__name__))
                    return True
                else:
                    print('La clave no coincide \n')
                    return False

        print('Usuario no econtrado \n')
        return False

    def dar_permiso(self, alumno, sigla):
        """
        Da permiso al alumno para poder tomar el ramo con la sigla especificada
        :param alumno: str con el nombre del alumno
        :param sigla: str con la sigla del curso
        :return True si es que se realizo con exito la accion
        """

        go = True
        for persona in self.personas:
            if persona.nombre == alumno and go:
                persona.permiso = sigla
                print('Permiso otorgado correctamente')
                return True
        print('Alumno no encontrado')
        return False

    def quitar_permiso(self, alumno, sigla):
        """
        Quita el permiso alguna vez otrogado y hace que el alumno bote el ramo
        :param alumno: Objeto tipo Alumno
        :param sigla: objeto tipo str
        """

        for persona in self.personas:
            if persona.nombre == alumno and persona.permiso == sigla:
                alumno = persona
                alumno.permiso = 'Ninguno'
        for curso in alumno.cursos_por_tomar:
            if curso.sigla == sigla and not self.cumple_requisitos(alumno, curso):
                self.retirar_curso(alumno, curso)

    def buscar_curso(self, nrc):
        """
        Dado un codio NRC busca alguna coincidencia con los cursos de la lista
        :param nrc: objeto tipo int
        :return: objeto tipo curso or False
        """
        for curso in self.cursos:
            if nrc == curso.nrc:
                print('Curso encontrado', curso)
                return curso
        print('No existe un curso con ese NRC')
        return False

    def inscribir_curso(self, alumno, curso):
        """
        Revisa todas las condiciones necesarias para poder tomar un curso y luego se le asigna el curso al alumno
        :param alumno: objeto tipo Alumno
        :param curso: objeto tipo Curso
        :return: agrega alumno a la lista de curso, agrega el curso a la carga del alumno y resta una vacante del curso
        """
        if alumno.creditos_inscritos + curso.creditos <= alumno.creditos_maximos:
            if self.hay_vacantes(curso):
                if self.cumple_requisitos(alumno, curso):  # or alumno.permiso == curso.sigla:
                    if not alumno.cursos_por_tomar or not self.tope_de_horario(alumno, curso):
                        if not self.tope_de_evaluaciones(alumno, curso):
                            curso.lista_alumnos.append(alumno)
                            alumno.cursos_por_tomar.append(curso)
                            print('Curso agregado exitosamente \n')
                        else:
                            print('Error: existe tope de evaluacion con {}'.format(self.tope_de_horario(alumno, curso)))
                    else:
                        print('Error: existe tope de horario con {}'.format(self.tope_de_horario(alumno, curso)))
                else:
                    print('Error: No cumple con los requisitos del curso')
            else:
                print('Error: No hay vacantes disponibles')
        else:
            print('Error: Exede los creditos maximos que puede tomar')

    @staticmethod
    def calcular_grupo(n, x):
        """
        Calcula el grupo de banner segun el numero n
        :param n: Bacanosidad del alumno
        :param x: Vector de bacanosidad calculado con page_Rank
        :return: Un objeto int que representa el numero del grupo
        """
        min = bacanosidad_min(x)
        delta = (1 - min) / 10
        if min <= n and n <= min + delta:
            return 10

        elif min + delta < n and n <= min + 2 * delta:
            return 9

        elif min + 2 * delta < n and n <= min + 3 * delta:
            return 8

        elif min + 3 * delta < n and n <= min + 4 * delta:
            return 7

        elif min + 4 * delta < n and n <= min + 5 * delta:
            return 6

        elif min + 5 * delta < n and n <= min + 6 * delta:
            return 5

        elif min + 6 * delta < n and n <= min + 7 * delta:
            return 4

        elif min + 7 * delta < n and n <= min + 8 * delta:
            return 3

        elif min + 8 * delta < n and n <= min + 9 * delta:
            return 2

        elif min + 9 * delta < n and n <= min + 10 * delta:
            return 1

    @staticmethod
    def retirar_curso(alumno, curso):
        """
        El alumno remueve se su carga academica el curso
        :param alumno: objeto tipo Alumno
        :param curso: objeto tipo Curso
        :return: quita al alumno de la lista del curso, quita el curso de la carga academica del alumno,
        aumenta la capacidad del curso en 1
        """
        if alumno.cursos_por_tomar and curso in alumno.cursos_por_tomar:
            curso.lista_alumnos.remove(alumno)
            alumno.cursos_por_tomar.remove(curso)
            print('Curso retirado exitosamente')

    @staticmethod
    def cumple_requisitos(alumno, curso):
        """
        Comprueba si es que el alumno ha aprobado algun set de los requisitos del curso NOTA: por simplicidad los
        COrequisitos los considere como requisitos estrictos.
        :param alumno: objeto tipo Alumno
        :param curso: objeto tipo Curso
        :return: boolean si es que el alumno cumple los requisitos
        """

        if len(curso.requisitos) > 0:
            for item in curso.requisitos:
                go = True
                for req in item:
                    if req not in alumno.cursos_aprobados:
                        go = False
                if go:
                    return True
            return False
        return True

    @staticmethod
    def hay_vacantes(curso):
        """
        Revisa si que quedan vacantes en el curso
        :param curso: objeto tipo Curso
        :return: boolean
        """
        if curso.disponibles > 0:
            return True
        return False

    @staticmethod
    def tope_de_horario(alumno, curso):
        """
        Revisa si es que el alumno tiene o no tope de horario al momento de inscribir el curso
        :param alumno: objeto tipo Alumno
        :param curso: objeto tipo Curso
        :return: objeto tipo Curso
        """
        for horario in curso.horario:
            for ramo in alumno.cursos_por_tomar:
                if horario in ramo.horario:
                    return ramo
        return ''

    @staticmethod
    def tope_de_evaluaciones(alumno, curso):
        """
        Revisa si es que el alumno tiene o no tope de evaluaciones al momento de inscribir el curso
        :param alumno: objeto tipo Alumno
        :param curso: objeto tipo Curso
        :return: objeto tipo Curso
        """
        for evaluacion in curso.evaluaciones:
            for ramo in alumno.cursos_por_tomar:
                for i in ramo.evaluaciones:
                    if evaluacion.fecha == i.fecha:
                        return ramo
        return ''

