from estructuras import Lista, Deque


def bfs(G, v):
    """
    Algoritmo de busqueda en amplitud para grafos inventado por Edward F. Moore en 1950
    La idea es para cada u en G asignarle d(v,u) e ir guardando el camino que vamos siguiendo.
    :param G: Una lista de objetos tipo Nodo (o Puerto)
    :param v: Objeto tipo Nodo (o Puerto)
    """
    for nodo in G:
        nodo.distancia = 100000
        nodo.visto = False
        nodo.padre = None

    cola = Deque()
    v.distancia = 0
    v.visto = True
    cola.append(v)

    while cola:
        u = cola.popleft()
        for nodo in u.lista_vecinos:
            if not nodo.visto:
                nodo.distancia = u.distancia + 1
                nodo.padre = u
                cola.append(nodo)
                nodo.visto = True


def doble_sentido(G):
    for nodo in G:
        nodo.visto = False

    lista = Lista()

    def dfs(v):

        caminos = Lista()
        for nodo in G:
            nodo.padre = None

        stack = Lista()
        v.visto = True
        stack.append(v)

        while stack:

            u = stack.pop()

            for w in u.lista_vecinos:
                if not w.visto and conected(w, u):
                    w.visto = True
                    w.padre = u
                    stack.append(w)
            camino = backtrack(u)
            if len(camino) > 1:
                caminos.append(backtrack(u))

        return caminos

    for i in range(len(G)):
        if not G[i].visto:
            lista += dfs(G[i])

    return lista


def conected(u, v):
    if v in u.lista_vecinos:
        return True
    return False


def backtrack(v):
    """
    Algortimo recursivo para encontrar el camino desde v hasta 0
    :param v: Objeto del tipo Nodo (o Puerto)
    :return: Objeto del tipo list, que es el camino ivertido mas corto desde el vertive v hasta el vertice 0
    """
    camino = Lista()
    camino.append(v)

    if v.padre:
        camino += backtrack(v.padre)
    return camino


def find_path(G, s, t):
    def quedan_vecinos(v):
        for u in v.lista_vecinos:
            if u.color == 'W':
                return True
        return False

    for nodo in G:
        nodo.padre = None
        if nodo.color == 'G':
            nodo.color = 'W'

    s.color = 'G'
    stack = Lista()
    stack.append(s)

    while stack:
        u = stack.pop()
        for nodo in u.lista_vecinos:
            if nodo.color == 'W':
                nodo.color = 'G'
                nodo.padre = u
                stack.append(nodo)
                print(quedan_vecinos(nodo))
                if not quedan_vecinos(nodo):
                    nodo.color = 'B'

    return backtrack(t)


if __name__ == '__main__':  # Estas lineas las use para probar los algoritmos de busquda
    class Nodo:
        def __init__(self, nombre, capacidad):
            self.nombre = nombre
            self.lista_vecinos = Lista()
            self.distancia = None
            self.padre = None
            self.visto = False
            self.calculado = False
            self.capacidad = capacidad
            self.color = 'W'

        def agregar_vecino(self, *nodos):
            for nodo in nodos:
                self.lista_vecinos.append(nodo)

        def __repr__(self):
            return '{0}'.format(self.nombre)
