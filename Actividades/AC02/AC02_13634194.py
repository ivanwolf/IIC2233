class Audifonos():
    def __init__(self, freq_max='', freq_min='', imperancia='', intensidad='', **kwargs):
        self.freq_max = freq_max
        self.freq_min = freq_min
        self.imperancia = imperancia
        self.intensidad = intensidad

    def escuchar(self, song):
        if type(self) == Inalambrico:
            print('la cancion ' + song + ' esta siendo reproducida desde un audifono inalambrico')
        elif type(self) == Bluetooth:
            print('la cancion ' + song + ' esta siendo reproducida desde un audifono Bluetooth')
        else:
            print('la cancion ' + song + ' esta siendo reproducida desde un audifono')


class OverEar(Audifonos):
    def __init__(self, aislacion, **kwargs):
        super().__init__(**kwargs)
        self.aislacion = aislacion


class Intraaurales(Audifonos):
    def __init__(self, incomodidad, **kwargs):
        super().__init__(**kwargs)
        self.incomodidad = incomodidad


class Inalambrico(Audifonos):
    def __init__(self, rango, **kwargs):
        super().__init__(**kwargs)
        self.rango = rango

    def conectarse(self, distancia):
        if distancia <= self.rango:
            print('Audifono conectado exitosamente')
        else:
            print('Error: Audifono fuera de rango')


class Bluetooth(Inalambrico):
    def __init__(self, id, **kwargs):
        super().__init__(**kwargs)
        self.id = id


a = OverEar(100, freq_min=50, freq_max=60, imperancia=3, intensidad=100)
c = Inalambrico(13, freq_min=12, freq_max=40, imperancia=1, intensidad=123)
b = Intraaurales(34, freq_min=123, freq_max=1400, imperancia=2, intensidad=222)
d = Bluetooth(1, freq_min=111, freq_max=200, imperancia=4, intensidad=400, rango=5)

a.escuchar('Porter Robnson - Divinity')
b.escuchar('Porter Robinson - Fresh Static Snow')
c.escuchar('Madeon - Home')
d.escuchar('Au5 - Inside')

c.conectarse(9)
d.conectarse(6)
