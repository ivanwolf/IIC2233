import random


def posible_cfg(radar, barco):
    def pos_correcta(radar, pos):
        if pos[0] not in range(radar.largo) or pos[1] not in range(radar.largo):
            return False

        if radar[pos[1], pos[0]] in ['B', 'L', 'P', 'X', 'U']:
            return False
        return True

    def ubi_correcta(radar, ubicacion):
        """
        Revisa que cada posicion de la lista ubicacion sea correcta
        :param radar: Radar()
        :param ubicacion: lista con las posiciones
        :return: boolean
        """
        for pos in ubicacion:
            if not pos_correcta(radar, pos):
                return False
        return True

    def ubicacion(area, pos):
        return [(pos[0] + i, pos[1] + j) for i in range(area[0]) for j in range(area[1])]

    radar = radar.copy()
    hits = radar.hits
    area = barco.area_utilizada
    largo = radar.largo
    radares_posibles = []

    cabezas = []
    if hits:
        for hit in hits:
            cabezas += [(hit[0] - i, hit[1] - j) for i in range(area[0]) for j in range(area[1])]
    else:
        cabezas = [(i, j) for i in range(largo) for j in range(largo) if pos_correcta(radar, (i, j))]

    lista = list(filter(lambda pos: pos_correcta(radar, pos), cabezas))
    lista = [ubicacion(area, pos) for pos in lista if ubi_correcta(radar, ubicacion(area, pos))]

    for item in lista:
        posible = radar.copy()
        for pos in item:
            posible.marcar(repr(barco)[0], pos)

        go = True
        for tab in radares_posibles:
            if tab.equivalentes(posible):
                go = False
        if go:
            radares_posibles.append(posible)
        del posible

    return radares_posibles


def contar(conteo, radar, tablero):
    for i in range(radar.largo):
        for j in range(radar.largo):
            if tablero[i, j] in ['B', 'L', 'P'] and radar[i, j] != 'O' and radar[i, j] != 'X':
                conteo[i][j] += 1


def mejor_opcion(conteo):
    """
    Retorna la posicion en la que sea mas probable encontrar un barco, i.e. la posicion en la cual
    el conteo sea mayor. Si el maximo se encuentra en mas de una poscion, se entregara una posicion
    aleatoria entre las mejores
    :param conteo: Matriz (lista de listas) de nxn donde A[i,j] representa la cantidad de apraiciones
    de la posicion
    :return: tuple x,y mejor opcion para disparar
    """
    maximo = 0
    opciones = []
    for i in range(len(conteo)):
        for j in range(len(conteo)):
            if conteo[i][j] >= maximo:
                maximo = conteo[i][j]

    for i in range(len(conteo)):
        for j in range(len(conteo)):
            if conteo[i][j] == maximo:
                opciones.append((j, i))

    return random.choice(opciones)


def recursion(barco, lista_cfg, lista_barcos, db, radar):
    hojas = []
    if not lista_barcos:
        for cfg in lista_cfg:

            for hoja in posible_cfg(cfg, barco):
                hojas.append(hoja)
                contar(db, radar, hoja)
    else:
        mapas = []
        for item in lista_barcos:
            aux = lista_barcos.copy()
            aux.remove(item)
            for cfg in lista_cfg:
                mapas += recursion(item, posible_cfg(cfg, barco), aux, db, radar)
        return mapas

    return hojas
