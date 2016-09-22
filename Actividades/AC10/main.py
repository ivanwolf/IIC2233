class RestrictedAccess(type):
    def __new__(cls, nombre, base_clases, diccionario):
        atributos = diccionario['attributes']
        del diccionario['attributes']

        def __init__(self, *args):
            dic = atributos
            for i in range(len(dic)):
                setattr(self, dic[i], args[i])

        diccionario.update({'__init__': __init__})

        return super().__new__(cls, nombre, base_clases, diccionario)


class Person(metaclass=RestrictedAccess):
    attributes = ["name", "lastname", "alias"]


p = Person('Ivan', 'Wolf', 'hola')
p.name = 'hola'
print(p.name)
