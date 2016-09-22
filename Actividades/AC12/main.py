class Bummer:
    def __init__(self):
        self.alumnos = {"Vicente Besa": Alumno("vabesa", 12345),
                        "Juan Pablo Schele": Alumno("jpschele", 54321),
                        "Ariel Seisdedos": Alumno("robocop6", 123456789)}

        self.ramos = [Ramo("IIC2133", 10), Ramo("ING2030", 100),
                      Ramo("ICH1104", 100), Ramo("IIC2143", 30),
                      Ramo("IIC2413", 30)]

        self.conectado = False

    def ingresar(self, usuario, clave):
        if not self.conectado:
            try:
                if self.alumnos[usuario].clave == clave:
                    self.usuario_actual = self.alumnos[usuario]
                    self.conectado = True
                    print("Se conecto {0}".format(self.usuario_actual.usuario))
            except KeyError:
                print('KeyError')
                print('{0} no se encuentra en la lista de Alumnos'.format(usuario))

    def inscribir_ramo(self, numero):

        if self.conectado:
            try:
                ramo_inscribir = self.ramos[numero]
                if ramo_inscribir.vacantes > 0:
                    self.usuario_actual.agregar_ramos(ramo_inscribir)
                    print("Se inscribio el curso de sigla {0} a {1}".format(ramo_inscribir.sigla,
                                                                            self.usuario_actual.usuario))
            except IndexError:
                print('IndexError')
                print('Solo hay 5 ramos enumerados del 0 al 4, se ingreso {}'.format(numero))
            except TypeError:
                print('TypeError')
                print('Para inscribir un ramo hay que ingresar su NCR (int), se ingreso una sigla (str)'
                      '{0}'.format(numero))

    def quitar_ramo(self, numero):
        if self.conectado:
            try:
                ramo_quitar = self.ramos[numero]

                self.usuario_actual.quitar_ramos(ramo_quitar.sigla)
                print("Se quito el curso de sigla {0} de la carga academica de {1}".format(ramo_quitar.sigla,
                                                                                           self.usuario_actual.usuario))
            except KeyError:
                print('KeyError')
                print('El curso con NCR:{0} no se encuentra en la lista de ramos'.format(numero))

            except IndexError:
                print('IndexError')
                print('Solo hay 5 ramos enumerados del 0 al 4, se ingreso {}'.format(numero))
            except TypeError:
                print('TypeErro')
                print('Para inscribir un ramo hay que ingresar su NCR (int), se ingreso una sigla (str)'
                      '{0}'.format(numero))

    def calificar(self, numero, nota):
        try:
            if self.conectado:
                ramo = self.ramos[numero]
                self.usuario_actual.calificar_curso(ramo.sigla, nota)
                print("Se califico a {} en el curso {} con la nota {}".format(self.usuario_actual.usuario, ramo.sigla,
                                                                              nota))
        except ValueError:
            print('ValueError')
            print('La nota debe ser entera (int) y no un string')

        except KeyError:
            print('KeyError')
            print('El curso con NCR:{0} no se encuentra en la lista de ramos'.format(numero))

        except IndexError:
            print('IndexError')
            print('Solo hay 5 ramos enumerados del 0 al 4, se ingreso {}'.format(numero))
"""

No se puede modificar desde aquí

"""


class Ramo:
    def __init__(self, sigla, vacantes):
        self.sigla = sigla
        self.vacantes = vacantes
        self.alumnos = {}

    def inscrito(self, alumno):
        self.vacantes -= 1
        self.alumnos[alumno.usuario] = alumno


class Alumno:
    def __init__(self, usuario, clave):
        self.usuario = usuario
        self.clave = clave
        self.ramos = {}
        self.ramos_aprobados = {}

    def agregar_ramos(self, ramo):
        self.ramos[ramo.sigla] = ramo
        ramo.inscrito(self)

    def quitar_ramos(self, sigla):
        del self.ramos[sigla]

    def calificar_curso(self, sigla, nota):
        ramo = self.ramos[sigla]
        nota = float(nota)
        self.ramos_aprobados[sigla] = (ramo, nota)


if __name__ == '__main__':
    bummer = Bummer()
    bummer.ingresar("Marco Bucchi", 12345)
    bummer.ingresar("Juan Pablo Schele", 54321)
    bummer.inscribir_ramo(5)
    bummer.inscribir_ramo(0)
    bummer.inscribir_ramo("IIC2111")
    bummer.inscribir_ramo(2)
    bummer.quitar_ramo(0)
    bummer.quitar_ramo("Investigación")
    bummer.quitar_ramo(4)
    bummer.quitar_ramo(5)
    bummer.calificar(2, "siete")
    bummer.calificar(0, "7.0")
    bummer.calificar(2, "7.0")
    bummer.calificar(5, "1.0")
