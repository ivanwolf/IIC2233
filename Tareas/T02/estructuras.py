class Nodo:
    def __init__(self, valor=None, padre=None):
        self.padre = padre
        self.siguiente = None
        self.valor = valor

    def __repr__(self):
        return 'Nodo:{}'.format(self.valor)


class Lista:
    def __init__(self, *args):

        self.cabeza = None
        self.cola = None
        self.largo = 0
        for arg in args:
            self.append(arg)

    def __repr__(self):

        if not self.cabeza:
            return '[]'
        rep = '['
        for item in self:
            rep += '{0}, '.format(item)
        return rep[:-2] + ']'

    def __next__(self):

        item = self.item
        if not item:
            raise StopIteration
        self.item = self.item.siguiente
        return item.valor

    def __iter__(self):

        self.item = self.cabeza
        return self

    def __len__(self):

        return self.largo

    def __getitem__(self, ide):

        if ide > len(self) - 1:
            raise IndexError('Indice de la lista fuera de rango')

        item = self.cabeza
        for i in range(ide):
            item = item.siguiente
        return item.valor

    def __setitem__(self, ide, value):

        if ide > len(self) - 1:
            raise IndexError('Indice de la lista fuera de rango')

        item = self.cabeza
        for i in range(ide):
            item = item.siguiente
        item.valor = value

    def __bool__(self):

        if len(self) == 0:
            return False
        return True

    def __contains__(self, item):

        for obj in self:
            if obj == item:
                return True
        return False

    def __add__(self, other):

        lista = Lista()
        for item in self:
            lista.append(item)
        for item in other:
            lista.append(item)
        return lista

    def append(self, valor):
        if not self.cabeza:
            self.cabeza = Nodo(valor)
            self.cola = self.cabeza
        else:
            self.cola.siguiente = Nodo(valor, self.cola)
            self.cola = self.cola.siguiente
        self.largo += 1

    def pop(self):
        item = self.cola
        if len(self) == 1:
            self.cabeza = None
            self.cola = None
            self.largo = 0
            return item.valor

        self.cola = self.cola.padre
        self.cola.siguiente = None
        self.largo -= 1
        return item.valor

    def copy(self):
        copia = Lista()
        for item in self:
            copia.append(item)
        return copia


class Tupla:
    def __init__(self, *args):
        self.data = Lista()
        for valor in args:
            self.data.append(valor)

    def __repr__(self):
        return '(' + str(self.data).lstrip('[').rstrip(']') + ')'

    def __getitem__(self, ide):
        if ide > len(self.data):
            raise IndexError('Indice de la tupla fuera de rango')
        return self.data[ide]

    def __contains__(self, item):
        return item in self.data

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return iter(self.data)


class Dict:
    def __init__(self, numentradas):
        """
        Crea una tabla de hash con n entradas
        :param numentradas: objeto tipo int
        """
        self.numentradas = numentradas
        self.casillas = Lista()

        self.keys = Lista()
        self.values = Lista()
        self.items = Lista()

        for i in range(numentradas):
            self.casillas.append(Lista())

    def __getitem__(self, key):
        """
        :param key: Objeto tipo int
        """
        casilla = self.casillas[self.hash_function(key)]
        for item in casilla:
            if item[0] == key:
                return item[1]
        raise KeyError('Llave no encontrada')

    def __setitem__(self, key, value):
        """
        Las keys solo pueden ser nuero enteros
        :param key: objeto tipo int
        :param value: ojeto que guardaremos
        """
        casilla = self.casillas[self.hash_function(key)]

        for i in range(len(casilla)):
            if casilla[i][0] == key:
                casilla[i] = Tupla(key, value)
                return True

        casilla.append(Tupla(key, value))
        self.keys.append(key)
        self.values.append(value)
        self.items.append(Tupla(key, value))

    def __repr__(self):
        if not self:
            return '{}'
        rep = '{'
        for casilla in self.casillas:
            for item in casilla:
                rep += '{0}: {1}, '.format(item[0], item[1])
        return rep[:-2] + '}'

    def __len__(self):
        suma = 0
        for casilla in self.casillas:
            suma += len(casilla)
        return suma

    def __bool__(self):
        for casilla in self.casillas:
            if casilla:
                return True
        return False

    def __contains__(self, key):
        casilla = self.casillas[self.hash_function(key)]
        for item in casilla:
            if item[0] == key:
                return True
        return False

    def __iter__(self):
        return iter(self.keys)

    def hash_function(self, n):
        return n % self.numentradas


class Deque(Lista):
    def popleft(self):
        item = self.cabeza
        if len(self) == 1:
            self.cabeza = None
            self.cola = None
            self.largo = 0
            return item.valor

        self.cabeza = self.cabeza.siguiente
        self.cabeza.padre = None
        self.largo -= 1
        return item.valor
