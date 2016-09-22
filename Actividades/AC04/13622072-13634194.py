# coding=utf-8


# Completen los métodos
# Les estamos dando un empujoncito con la lectura del input
# Al usar la clausula: "with open('sonda.txt', 'r') as f", el archivo se cierra automáticamente al salir de la función.


def sonda():
    lista = []
    imprime = False
    mineral = ''
    with open('sonda.txt', 'r') as f:
        for line in f:
            lista.append(tuple(line.split(',')))

    n = int(input('Numero de consultas: '))

    for i in range(n):
        consulta = tuple((input('Posicion: ').split((','))))  # Tiene que ser de la forma x,y,z,w

        for element in lista:
            # for i in range(4):  ##Revisa las 4 posiciones
            if consulta[0] == element[1] and consulta[1] == element[1] and element[2] == consulta[2] and element[3] == \
                    consulta[3]:
                imprime = True
            else:
                imprime = False
            mineral = element[4]
        if imprime:
            print(mineral)
        else:
            print('No hay nada')

def traidores():
    bufalos = []
    with open('data/bufalos.txt', 'r') as f:
        for line in f:
            bufalos.append(line.strip())

    rivales = []
    with open('data/rivales.txt', 'r') as f:
        for line in f:
            rivales.append(line.strip())
    traidores = set()
    for i in range(len(bufalos)):
        for n in range(len(rivales)):
            if bufalos[i] == rivales[n]:
                traidores.add(bufalos[i])
    for i in traidores:
        print(i)


def pizzas():
    apiladas = []
    pizza = 1
    cola = []
    with open('data/pizzas.txt', 'r') as f:
        for line in f.read().splitlines():
            if line == 'APILAR':
                apiladas.append((line, pizza))
                print('Pizza {} apilada,{} Pizza Apilada - {}Pizzas en cola'.format(pizza, len(apiladas), len(cola)))
                pizza += 1
            elif line == 'ENCOLAR':
                sacada = apiladas.pop()
                cola.append(sacada)
                print(
                    'Pizza {} encolada,{} Pizza Apilada - {}Pizzas en cola'.format(sacada[1], len(apiladas), len(cola)))
            elif line == 'SACAR':
                sacando = cola.pop()
                print(
                    'Pizza {} sacada,{} Pizza Apilada - {}Pizzas en cola'.format(sacando[1], len(apiladas), len(cola)))


if __name__ == '__main__':
    exit_loop = False

    functions = {"1": sonda, "2": traidores, "3": pizzas}

    while not exit_loop:
        print(""" Elegir problema:
            1. Sonda
            2. Traidores
            3. Pizzas
            Cualquier otra cosa para salir
            Respuesta: """)

        user_entry = input()

        if user_entry in functions:
            functions[user_entry]()
        else:
            exit_loop = True
