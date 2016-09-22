def obtener_datos(path):
    """
    Lee el arhivo y lo evalua
    :param path: direccion y nombre del archivo a leer
    :return: Una lista donde cada elemento es un diccionario
    """
    with open(path, 'r', encoding='utf-8') as file:
        lista = file.readlines()

    datos = []

    for i in range(len(lista)):
        if '{' in lista[i]:
            s = ''
            try:
                j = lista.index('  },\n', i + 1)
            except ValueError:
                j = lista.index('  }\n', i + 1)

            for k in range(i, j + 1):
                if '\n' != lista[k]:
                    s += lista[k].replace(', ', '$ ').replace('\n', '').replace('  ', '')  # .replace('"', "'")

            datos.append(evaluar(encuentra_lista(s.strip(','))))

    return datos


def encuentra_lista(string):
    """
    :param string: de la forma "{'key_1': 'value_1','key_2': ..}" pero con la apraicion de una lista en lo valores
    :return: una copia del str pero cambiando las comas de la lisa por '%'
    """
    aux = string
    for i in range(len(string)):
        if string[i] == ',':
            if (string.count('[', 0, i) + string.count(']', 0, i)) % 2 != 0 or string[i + 1].isdigit():
                aux = aux[:i] + aux[i].replace(',', '%') + aux[i + 1:]

    return aux


def evaluar(string):
    """
    Evalua un str escrito en formato similar a json NOTA: probablemte no corra con string que no sean los de los
    archivos de la tarea
    :param string: objeto tipo str
    :return: objeto tipo dict
    """
    string = string.lstrip('{').rstrip('}')
    lista = string.split(',')
    lista_1 = []
    dic = {}

    for element in lista:
        par = element.split(': ')
        lista_1 += [par]

    for par in lista_1:

        par[0] = par[0].strip('"')
        par[1] = par[1].strip('"')
        if par[1] == '[]':
            par[1] = []
        elif '[' in par[1] and ']' in par[1]:
            par[1] = par[1].lstrip('[').rstrip(']').replace('"', '').split('%')
        elif '%' in par[1]:
            par[1] = par[1].replace('%', ',')
        elif '$' in par[1]:
            par[1] = par[1].replace('$', ',')
        elif par[1].isdigit():
            par[1] = int(par[1])
        dic.update({par[0]: par[1]})
    return dic


