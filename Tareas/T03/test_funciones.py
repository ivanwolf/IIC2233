import unittest
from funciones import esta_en_el_tablero, ask_fila, ask_position, ask_number, ask_attack
from ataque import MisildeCrucero
from jugador import Jugador


class TestEstaEnElTablero(unittest.TestCase):
    def test_esta_en_el_tablero(self):
        """ Verifica si es que la posicion esta dentro de los margenes del  0 hasta n-1 """
        n = 10
        pos_buena = [(i, j, 0) for i in range(n) for j in range(n)]
        for p in pos_buena:
            self.assertTrue(esta_en_el_tablero(p, n))
        pos_mala = (n, n, 0)
        self.assertFalse(esta_en_el_tablero(pos_mala, n))
        pass


class TestAskFila(unittest.TestCase):
    def test_ask_fila(self):
        """ Que pasa si no entregamos el formato pedido? formato: 'c,n' y 'f,n' """
        self.assertRaises(KeyError, ask_fila, 'b,3', 10)
        self.assertRaises(IndexError, ask_fila, 'c,14', 10)
        self.assertRaises(ValueError, ask_fila, 'c,a', 10)

        self.assertTrue(ask_fila('f,4', 10) == ('f', 4))
        # self.assertRaises(RuntimeError, ask_fila, 'f14', 10)


class TestAskPosition(unittest.TestCase):
    def test_ask_position_formato(self):
        """ Que pasa si no entregamos un formato de poscion valido? formato: x,y """
        self.assertRaises(KeyError, ask_position, '333aa', 0, 10)
        self.assertRaises(ValueError, ask_position, '3,', 0, 10)
        self.assertRaises(ValueError, ask_position, ',3', 0, 10)
        self.assertRaises(ValueError, ask_position, '1a,2b', 0, 10)

        self.assertTrue(ask_position('1,1', 0, 10) == (1, 1, 0))

    def test_ask_position_rango(self):
        """ Que pasa si entregamos una posicion valida pero fuera del tablero? """
        self.assertRaises(IndexError, ask_position, '12,3', 0, 9)


class TestAskNumber(unittest.TestCase):
    def test_ask_number_non_digit(self):
        """ Que pasa si le entregamos un string que no sea un digito"""

        self.assertRaises(ValueError, ask_number, 'aaa', 3)

        self.assertTrue(ask_number('2', 4) == 2)

    def test_ask_number_fuera_de_rango(self):
        """ Que pasa si le ingresamos un numero mayor a m """
        self.assertRaises(IndexError, ask_number, '5', 3)


class TestAskAttack(unittest.TestCase):
    def setUp(self):
        self.jugador = Jugador()
        self.arsenal = {'MC': MisildeCrucero()}

    def test_ask_attack_llave_incorrecta(self):
        """ Que pasa si el input no corresponde a una llave del arsenal? """
        self.assertRaises(KeyError, ask_attack, 'aaa', self.arsenal, 4)

        self.assertTrue(ask_attack('MC', self.arsenal, 4) == self.arsenal['MC'])

    def test_ask_attack_ataque_no_disponible(self):
        """ Que pasa si intento usar un ataque no disponible"""

        ataque = self.arsenal['MC']
        ataque.ultima_vez = 1  # Suponemos que usamos el ataque en el turno 1
        self.jugador.turno = 2  # En el turno dos el ataque no deberia estar disponible
        self.assertRaises(PermissionError, ask_attack, 'MC', self.arsenal, self.jugador.turno)

        ataque.ultima_vez = 0  # Suponemos que nunca hemos usado el ataque
        self.assertTrue(ask_attack('MC', self.arsenal, self.jugador.turno) == self.arsenal['MC'])


if __name__ == "__main__":
    unittest.main()
