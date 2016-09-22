import sistema as sis
from clases import Red, Puerto

__author__ = 'ivanwolf'


def generar_red():
    """
    La idea es abrcar lo mas que se pueda la red que desconocemos e ir guardando el camino que vamos tomando para que
    efectivamente el programa pueda tarminar. Mi programa se dentendra cuando hayamos visitado el puerto de bummer
    un numero determinado de veces. Los problemas que tiene este algoritmo son que el tiempo de ejecucion es variable
    y que se segura que hayamos visto el 100% de los nodos, sin embargo, si la red tiene al rededor de 1200 nodos,
    al pasar 5 veces por bummer habremos encontrado aprox el 99% de los nodos.
    """
    red = Red()
    puerto_final_ide = sis.puerto_final()
    puerto_actual = Puerto(sis.puerto_inicio(), sis.posibles_conexiones(), sis.get_capacidad())
    i = 0
    red.agregar_puerto(puerto_actual)

    while i < 10:

        n = puerto_actual.proxima_conexion
        sis.hacer_conexion(n)
        puerto_anterior = puerto_actual
        m = sis.preguntar_puerto_actual()[0]
        atrapado = sis.preguntar_puerto_actual()[1]

        if m in red.puertos:
            puerto_actual = red.puertos[m]  # 1
        else:
            puerto_actual = Puerto(m, sis.posibles_conexiones(), sis.get_capacidad())

        red.agregar_puerto(puerto_actual, puerto_anterior, n, atrapado)  # 2

        if puerto_actual.ide == puerto_final_ide:
            puerto_actual.bummer = True
            print('Encontramos Bummer')
            i += 1

    print('Red Generada')
    return red


1
red = generar_red()
red.imprimir_red()
red.imprimir_prueba()
red.imprimir_ruta()
red.imprimir_rutas_dobles()
