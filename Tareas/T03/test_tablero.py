import unittest
from jugador import Jugador
from vehiculo import BuquedeGuerra, Kamikaze, Puerto, Lancha


class TestTableroUbicarVehiculo(unittest.TestCase):
    """
    Tests para para el metodo ubicar_vehiculo
    """

    def setUp(self):
        self.jugador = Jugador('ivan', n=8)
        self.tablero = self.jugador.tablero
        self.barco = BuquedeGuerra()
        self.lancha = Lancha()
        self.avion = Kamikaze()

    def test_ubicar_vehiculo(self):

        """Puedo ubicar un objeto que este completamente adentro del tablero?"""

        self.tablero.ubicar_vehiculo((0, 0, 0), self.barco)
        for p in self.barco.ubicacion:
            self.assertTrue(self.tablero[p] == self.barco)

        self.tablero.ubicar_vehiculo((0, 0, 1), self.avion)
        for p in self.avion.ubicacion:
            self.assertTrue(self.tablero[p] == self.avion)

    def test_ubicar_vehiculo_borde(self):

        """Que pasa si intento ubicar un vehiculo pero este es muy grande?"""

        self.assertRaises(IndexError, self.tablero.ubicar_vehiculo, (7, 7, 0), self.barco)

    def test_ubicar_vehiculo_sobre_otro(self):

        """Que pasa si intento ubicar un vehiluco en un lugar donde ya existe otro?"""

        self.tablero.ubicar_vehiculo((0, 0, 0), self.barco)
        for p in self.barco.ubicacion:
            self.assertRaises(RuntimeError, self.tablero.ubicar_vehiculo, p, self.lancha)


class TestTableroQuitarVehiculo(unittest.TestCase):
    def setUp(self):
        self.jugador = Jugador('ivan', n=8)
        self.tablero = self.jugador.tablero
        self.barco = BuquedeGuerra()
        self.lancha = Lancha()
        self.avion = Kamikaze()

    def test_quitar_vehiculo(self):
        """ Que pasara cuando un vehiculo sea destrudio"""

        self.tablero.ubicar_vehiculo((0, 0, 0), self.barco)
        self.tablero._quitar_vehiculo(self.barco)
        self.assertTrue(self.tablero[0, 0, 0] is None)
        self.tablero._quitar_vehiculo(self.avion)


class TestTableroMoverVehiculo(unittest.TestCase):
    def setUp(self):
        self.jugador = Jugador('ivan', n=8)
        self.tablero = self.jugador.tablero
        self.barco = BuquedeGuerra()
        self.puerto = Puerto()
        self.lancha = Lancha()
        self.avion = Kamikaze()

    def test_mover_vehiculo_movimientos_posibles(self):

        """ Se cumplen las restricciones de movimiento? """

        self.tablero.ubicar_vehiculo((2, 2, 0), self.barco)
        self.tablero.ubicar_vehiculo((0, 0, 0), self.puerto)

        self.assertRaises(RuntimeError, self.tablero.mover_vehiculo, (5, 5, 0), self.barco)
        self.assertRaises(PermissionError, self.tablero.mover_vehiculo, (10, 14, 0), self.puerto)

    def test_mover_vehiculo_eliminando_resgistro(self):

        """Cuando nos movemos, el tablero cambia la posicion del objeto?"""

        self.tablero.ubicar_vehiculo((0, 0, 0), self.lancha)
        antigua_ubicacion = self.lancha.ubicacion
        self.tablero.mover_vehiculo((4, 4, 0), self.lancha)

        for pos in antigua_ubicacion:
            self.assertTrue(self.tablero[pos] is None)

        for pos in self.lancha.ubicacion:
            self.assertTrue(self.tablero[pos] == self.lancha)

    def test_mover_vehiculo_posicion_incorrecta(self):

        """ Si intentamos mover una pieza afuera del tablero o encima de otra"""

        self.tablero.ubicar_vehiculo((0, 0, 0), self.puerto)
        self.tablero.ubicar_vehiculo((5, 5, 0), self.lancha)

        self.assertRaises(RuntimeError, self.tablero.mover_vehiculo, (0, 0, 0), self.lancha)
        self.assertRaises(IndexError, self.tablero.mover_vehiculo, (40, 40, 0), self.lancha)


if __name__ == "__main__":
    unittest.main()
