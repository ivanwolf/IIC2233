def adyacentes(objeto, plano):
    """
    :param objeto: Objeto tipo Calle, Casa
    :param plano: plano de una Ciudad
    :return: una lista con string que representan a los vecinos
    """
    i, j = objeto.i, objeto.j
    lista = []
    for n in {1, -1}:
        try:
            lista.append(repr(plano[i + n][j]))
        except IndexError:
            pass
    for n in {1, -1}:
        try:
            lista.append(repr(plano[i][j + n]))
        except IndexError:
            pass

    return lista


def distancia(p1, p2):
    x, y = abs(p1[0] - p2[0]), abs(p1[1] - p2[1])
    if x:
        return x - 1
    if y:
        return y - 1


def posicion_frente(vehiculo):
    i, j = vehiculo.i, vehiculo.j
    direccion = vehiculo.direccion

    if direccion == 'abajo':
        return i + 1, j
    if direccion == 'arriba':
        return i - 1, j
    if direccion == 'izquierda':
        return i, j - 1
    if direccion == 'derecha':
        return i, j + 1


def suma(par1, par2):
    return par1[0] + par2[0], par1[1] + par2[1]


def per(par):
    return -par[1], par[0]


def mul(n, par):
    return n * par[0], n * par[1]
