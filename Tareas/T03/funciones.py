def ask_position(inp, k, largo):
    """
    Revisa si es que el intput del usuario corresponde a una posicion valida x,y
    :param inp: str, input del usuario
    :param k: int, tercera coordenana de la posicon
    :param n: int, rango del tablero
    :return: tuple, posicion valida x,y
    :raises KeyError, ValueError, IndexError
    """
    if ',' not in inp:
        raise KeyError
    inp = inp.split(',')

    x, y = int(inp[0]), int(inp[1])
    if (x > largo - 1 or x < 0) or (y > largo - 1 or y < 0):
        print('Error: Esta coordenada esta fuera del teblero')
        raise IndexError

    return int(inp[0]), int(inp[1]), k


def ask_number(inp, m):
    """
    Si el input es un str entre 0 y m-1 retorna el input como entero
    :param inp: str, input ingresado por el ususario
    :param m: int, rango de aceptacion
    :return: int
    :raises IndexError, ValueError
    """
    if m == 0:
        return 0
    if int(inp) not in range(m):
        print('Necesitamos un numero entre 0 y {}'.format(m - 1))
        raise IndexError

    return int(inp)


def ask_attack(inp, diccionario, turno):
    """
    Retorna el ataque correspondiente a las siglas que ingrese el usuario, si es que
    esta disponible
    :param inp: str, input del ususario
    :param diccionario: dict
    :return: value
    :raises: KeyError, PermissionError
    """
    key = inp.upper()
    if not diccionario[key].disponible(turno)[0]:
        print('Error: Este ataque aun no esta disponible')
        raise PermissionError

    return diccionario[key]


def ask_fila(inp, n):
    """
    Si el input esta en el formato correcto retorna la tupla con la poscion correcta formato f,3
    :param inp: str, input ingresado por el usuario
    :param n: int, largo del tablero
    :return: (str, int)
    :raises KeyError, IndexError, ValueError
    """
    inp = inp.split(',')
    if len(inp) == 1:
        print('Un formato valido es por ejemplo "c,3"')
        raise KeyError

    if inp[0] != 'c' and inp[0] != 'f':
        print('La primera coordenanda tiene que ser "f" o "c"')
        raise KeyError

    if int(inp[1]) not in range(n):
        print('Estas seguro de que quieres atacar fuera del tablero?')
        raise IndexError

    return inp[0], int(inp[1])


def loop(func, param, exceptions, msg, error=''):
    """
    Le pide al usuario un input hasta que ingrese un formato correcto de acuerdo a la funcion func
    :param func: func, funcion que define un formato de input correcto
    :param param: list, parametros de la funcion func
    :param exceptions: Exeption, excepcion que levanta la funcion func
    :param msg: str, mensaje que se muestra cuando se pide un input
    :param error: str, mensaje que se muestra cuando se levanta una excepcion
    :return:
    """
    p = input(msg)
    while True:
        try:
            return func(p, *param)
        except exceptions:
            print(error)
            p = input(msg)


def esta_en_el_tablero(pos, n):
    """
    Verifica si es que la posicion esta dentro de los margenes del tablero
    :param pos: Tupla (x,y,z)
    :return: Bool
    """
    x, y, z = pos[0], pos[1], pos[2]
    if (x > n - 1 or x < 0) or (y > n - 1 or y < 0) or (z > 1 or z < 0):
        return False
    return True
