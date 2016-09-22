#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import pickle
import datetime


class Persona:
    def __init__(self, ide, nombre):
        self.id = ide
        self.nombre = nombre
        self.amigos = []
        self.persona_favorita = ''
        self.veces_guardado = 0
        self.fecha = None


def existe_persona(_id):
    archivos = os.listdir('db')
    if _id + '.iic2233' in archivos:
        return True
    return False


def get_persona(_id):
    if existe_persona(_id):
        with open('db/{0}.iic2233'.format(_id), 'rb') as file:
            persona = pickle.load(file)
        return persona
    print('La persona no exite')
    return None

def write_persona(persona):
    with open('db/{0}.iic2233'.format(persona.id), 'wb') as file:
        persona.fecha = datetime.datetime.now()
        persona.veces_guardado += 1
        pickle.dump(persona, file)


def crear_persona(_id, nombre_completo):
    if '.' in _id:
        print('No puede haber ides con puntos!!')
        return None
    persona = Persona(_id, nombre_completo)
    if not existe_persona(_id):
        with open('db/{0}.iic2233'.format(_id), 'wb') as file:
            persona.fecha = datetime.datetime.now()
            persona.veces_guardado += 1
            pickle.dump(persona, file)


def agregar_amigo(id_1, id_2):
    if existe_persona(id_1) and existe_persona(id_2):
        persona_1 = get_persona(id_1)
        persona_2 = get_persona(id_2)

        if not id_1 in persona_2.amigos:
            persona_2.amigos.append(id_1)

        if id_2 not in persona_1.amigos:
            persona_1.amigos.append(id_2)

        write_persona(persona_1)
        write_persona(persona_2)


def set_persona_favorita(_id, id_favorito):
    if existe_persona(_id) and existe_persona(id_favorito):
        persona = get_persona(_id)
        persona.persona_favorita = id_favorito
        write_persona(persona)


def get_persona_mas_favorita():
    # Las personas no pueden tener nombre con puntos
    lista = os.listdir('db')
    dict = {}
    for archivo in lista:
        ide = archivo.split('.')[0]
        persona = get_persona(ide)
        if persona.persona_favorita not in dict:
            dict.update({persona.persona_favorita: 1})
        else:
            dict[persona.persona_favorita] += 1

    per = max(dict, key=dict.get)
    return  get_persona(per).nombre, dict[per]

# ----------------------------------------------------- #
# Codigo para probar su tarea - No necesitan entenderlo #


def print_data(persona):
    if persona is None:
        print("[AVISO]: get_persona no está implementado")
        return

    for key, val in persona.__dict__.items():
        print("{} : {}".format(key, val))
    print("-" * 80)


# Metodo que sirve para crear el directorio db si no existia #

def make_dir():
    if not os.path.exists("./db"):
        os.makedirs("./db")


if __name__ == '__main__':

    make_dir()
    crear_persona("jecastro1", "Jaime Castro")
    crear_persona("bcsaldias", "Belen Saldias")
    crear_persona("kpb", "Karim Pichara")
    set_persona_favorita("jecastro1", "bcsaldias")
    set_persona_favorita("bcsaldias", "kpb")
    set_persona_favorita("kpb", "kpb")
    agregar_amigo("kpb", "jecastro1")
    agregar_amigo("kpb", "bcsaldias")
    agregar_amigo("jecastro1", "bcsaldias")

    jecastro1 = get_persona("jecastro1")
    bcsaldias = get_persona("bcsaldias")
    kpb = get_persona("kpb")

    print_data(jecastro1)
    print_data(bcsaldias)
    print_data(kpb)

    print(get_persona_mas_favorita())
