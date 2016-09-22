import numpy as np


def generar_lista_alumnos(lista_diccionarios):
    """
    Para cada diccionario en la lista si corresponde a un alumno, le agrega el par (id, i) para poder contarlos
     y retorna UN diccionario donde la key es el nombre del alumno y el value es el diccionario que extraimo del texto
     personas.txt
    :param lista_diccionarios: lista con los diccionarios parseados de personas.txt
    :return: Objeto del tipo dict
    """
    lista = {}
    i = 0
    for dic in lista_diccionarios:
        if dic['alumno'] == 'SI':
            dic.update({'id': i})
            lista.update({dic['nombre']: dic})
            i += 1
    return lista


def generar_matriz(lista_alumnos):
    """
    :param lista_alumnos: diccionario obtenido de la funcion generar_lista_alumnos()
    :return: Una matriz tal que A[i,j] = 0 si y solo si el alumno [j] NO sigue al alumno [i] y tal que las sumas de
    los elementos de cada columna es siempre 1
    """
    n = len(lista_alumnos)
    A = np.asmatrix(np.zeros((n, n)))

    for (key, value) in lista_alumnos.items():

        j = value['id']
        l = 1 / len(value['idolos'])

        columna_j = np.zeros((n, 1))
        for persona in value['idolos']:
            i = lista_alumnos[persona]['id']
            columna_j[i, 0] = 1

        A[:, j] = l * columna_j

    return A


def page_rank(A):
    """
    NOTA: Este algoritmo NO ES MIO, es una simplificacion que hice del algoritmo que tiene Google para clasificar las paginas
    llamado PageRank
    :param A: Una matriz (np.array) obtenida de la funcion generar_matriz
    :return: Un vector donde el numero de la componente i es la bacanosidad del alumno con id = i
    """
    epsilon = 0.0001
    error = 1
    n = len(A)
    x = (1 / n) * np.ones((n, 1))

    while error > epsilon:
        y = np.dot(A, x)
        error = np.linalg.norm(x - y)
        x = y

    return x


def agregar_bacanosidad(dic_alumnos, x):
    """
    Agrega la key 'bacanosidad' a los diccionarios sacados del texto personas.txt el value es la bacanosidad relativa
    :param dic_alumnos: Lista con objetos tipo dict
    :param x: np.array Es el vector obtenido despues de calcular bacanosidad con PageRank
    """

    for value in dic_alumnos.values():
        b = float(x[value['id']]) / float(np.amax(x))
        value.update({'bacanosidad': b})


def bacanosidad_min(x):
    return float(np.amin(x)) / float(np.amax(x))
