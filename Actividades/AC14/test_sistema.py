from main import Ramo, Base, Alumno


class TestSistema:
    def setup_method(self, method):
        self.base = Base()
        self.alumno = Alumno(self.base, 0, 'Ivan Wolf')

    def test_base_inscribir_hay_vacantes(self):
        """
        Se pueden tomar ramos si es que hay vacantes?
        """
        for ramo in self.base.db:
            assert self.base.inscribir(ramo.sigla, self.alumno)

    def test_base_inscribir_no_hay_vacantes(self):
        """
        Que pasa si no quedan bacantes?
        """
        for ramo in self.base.db:
            ramo.vacantes = 0
            assert not self.base.inscribir(ramo.sigla, self.alumno)

    def test_tomar_ramo_max_creditos(self):
        """
        Que pasa si ya tengo 50 cr
        """
        self.alumno.creditos_actuales = 45
        assert not self.alumno.tomar_ramo(self.base.db[1].sigla)

    def test_tomar_ramo_dos_veces(self):
        """
        Puede un alumno tomar el mismo ramo dos veces?
        """
        self.alumno.tomar_ramo(self.base.db[0].sigla)
        assert not self.alumno.tomar_ramo(self.base.db[0].sigla)

    def test_botar_ramo_libera_vacante(self):
        """
        Al botar un ramo, se libera una vacante?
        """
        curso = self.base.db[0]
        capacidad = curso.vacantes
        self.alumno.tomar_ramo(curso.sigla)
        self.alumno.botar_ramo(curso.sigla)

        assert capacidad == curso.vacantes

    def test_botar_ramo_eliminar_creditos(self):
        """
        Al botar un ramo se eliminan los creditos
        """
        curso = self.base.db[0]
        self.alumno.tomar_ramo(curso.sigla)
        creditos = self.alumno.creditos_actuales

        self.alumno.botar_ramo(curso.sigla)
        assert self.alumno.creditos_actuales == creditos - curso.creditos

    def test_botar_ramo_elimina_curos(self):
        """
        Al botar un ramo se elimina el curso de la lista de ramos del alumno
        """
        curso = self.base.db[0]
        self.alumno.tomar_ramo(curso.sigla)
        self.alumno.botar_ramo(curso.sigla)
        assert not curso in self.alumno.ramos
