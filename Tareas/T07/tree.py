class Nodo:
    def __init__(self, name, data, parent=None):
        self.name = name
        self.data = data
        self.padre = parent
        self.hijos = []
        self.visitado = False

    def __repr__(self):
        return self.name

class Tree:
    def __init__(self):
        nodo = Nodo('/', None)
        self.dict_nodos = {nodo.name: nodo}
        self.root = nodo

    def agregar_nodo(self, nodo_padre=None, nodo_hijo=None):
        if nodo_padre is not None and nodo_hijo is not None:
            nodo_padre.hijos.append(nodo_hijo)
            nodo_hijo.padre = nodo_padre
        self.dict_nodos.update({nodo_hijo.name: nodo_hijo})
