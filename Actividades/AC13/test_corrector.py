import unittest
from os import listdir
from main import Corrector


class TestCorrector(unittest.TestCase):
    def setUp(self):
        self.caso1 = Corrector("5435466-5_lucas_hidalgo.txt")
        self.caso2 = Corrector("6968271-5_Andrea_valdes.ttxtt")
        self.caso3 = Corrector("18936676-0_antonio_lopez.txt")
        self.caso4 = Corrector("18936677-k_rodrigo_lave.txt")
        self.casos = [self.caso1, self.caso2, self.caso3, self.caso4]

    def tearDown(self):
        for caso in self.casos:
            with open("Trabajos/" + caso.nombre, "rt") as file:
                lineas = file.readlines()[1:]
            with open("Trabajos/" + caso.nombre, "wt") as file:
                file.write("7.0\n")
                for linea in lineas:
                    file.write(linea)

    def test_revisar_nombre(self):

        self.assertTrue(self.caso1.revisar_nombre())
        self.assertTrue(self.caso2.revisar_nombre())
        self.assertTrue(self.caso3.revisar_nombre())
        self.assertFalse(self.caso4.revisar_nombre())

    def test_revisar_formato(self):
        self.assertTrue(self.caso1.revisar_formato(self.caso1.nombre))
        self.assertTrue(self.caso2.revisar_formato(self.caso2.nombre))
        self.assertTrue(self.caso1.revisar_formato('.txt'))
        self.assertFalse(self.caso1.revisar_formato('.pdf'))

    def test_revisar_verificador(self):
        self.assertTrue(self.caso1.revisar_verificador('5435466-5'))
        self.assertTrue(self.caso2.revisar_verificador('6968271-5'))
        self.assertTrue(self.caso3.revisar_verificador('18936676-0'))
        self.assertFalse(self.caso4.revisar_verificador('18936677-k'))

    def test_get_descuento(self):
        self.assertEqual(self.caso1.get_descuento(), 1)
        self.assertEqual(self.caso2.get_descuento(), 0)
        self.assertEqual(self.caso3.get_descuento(), 0)
        self.assertEqual(self.caso4.get_descuento(), 1)

    def test_revisar_orden(self):
        self.assertEqual(self.caso1.revisar_formato("5435466-5_lucas_hidalgo.txt"), True)
        self.assertEqual(self.caso2.revisar_formato("6968271-5_Andrea_valdes.ttxtt"), True)
        self.assertEqual(self.caso3.revisar_formato("18936676-0_antonio_lopez.txt"), True)
        self.assertEqual(self.caso4.revisar_formato("18936677-k_rodrigo_lave.txt"), True)

    def test_descontar(self):
        for caso in self.casos:
            caso.descontar()
            with open("Trabajos/" + caso.nombre, "rt") as file:
                nota = file.readline().strip()
            self.assertEqual(float(nota) == 7 - caso.descuento, True)

    def test_get_palabras(self):
        pass


suite = unittest.TestLoader().loadTestsFromTestCase(TestCorrector)
unittest.TextTestRunner().run(suite)
