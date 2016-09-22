from unittest import TestCase
from vehiculo import BarcoPequeno, Kamikaze


class TestVehiculoArea(TestCase):
    """
    Estamos calculando bien el area?
    """

    def test_area_marina(self):
        barco = BarcoPequeno()
        self.assertTrue(barco.area == [(0, 0, 0), (1, 0, 0), (2, 0, 0)])

    def test_area_aerea(self):
        kmz = Kamikaze()
        self.assertTrue(kmz.area == [(0, 0, 1)])

if __name__ == "__main__":
    unittest.main()