import requests

#
url = 'http://votaciometro.cloudapp.net/api/v1/'
user_pw = ('napoleon', 'macoy123')

class Table:
    def __init__(self, _id, name, votes):
        self.id = _id
        self.name = name
        self.votes = votes

    def __repr__(self):
        rep = 'id: {} \nname:{} \nvotes: {}\n'.format(self.id,
                                                    self.name,
                                                    self.votes)
        return rep

def get_listas(user, pw):
    response = requests.get(url + 'lists', auth=(user, pw))
    return response.json()

def get_mesas(user, pw):
    response = requests.get(url + 'tables', auth=(user, pw))
    return response.json()

def get_votos(user, pw):
    lista = []
    mesas = get_mesas(user, pw)
    ides = [mesa['_id'] for mesa in mesas]
    for _ide in ides:
        response = requests.get(url + 'tables/{}'.format(_ide), auth=(user, pw))
        lista.append(response.json())
    return lista

def crear_tables(mesas):
    lista_de_tables = []
    for item in mesas:
        name = item['name']
        ide = item['_id']
        votos = item['votes']
        lista_de_tables.append(Table(ide, name, votos))
    return lista_de_tables

def imprimir_ganador(tables):
    listas = get_listas(*user_pw)
    votes = []

    for lista in listas:
        votos = 0
        for table in tables:
            votos += table.votes[lista]
        votes.append((votos, lista))
    print('El ganador fue {1} con {0} votos'.format(*max(votes)))


if __name__ == '__main__':

    mesas = get_votos(*user_pw)
    tables = crear_tables(mesas)
    imprimir_ganador(tables)
