import socket
import threading
import time
import os
from collections import deque


class Cliente:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 3505
        self.s_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.conectar()
        except socket.error:
            print('No se conecto')

    def conectar(self):
        self.s_cliente.connect((self.host, self.port))
        self.escuchador = threading.Thread(target=self.escuchar, args=())
        self.escuchador.deamon = True
        self.escuchador.start()

    def escuchar(self):
        while True:
            data = self.s_cliente.recv(1024)


    def enviar(self, data):
        self.s_cliente.send(data.encode('utf-8'))

class Servidor:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 3505
        self.s_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_server.bind((self.host, self.port))
        self.s_server.listen(1)
        self.cliente = None

    def aceptar(self):
        new_client, addres = self.s_server.accept()
        self.cliente = new_client
        thread_cliente = threading.Thread(target=self.escuchar)
        thread_cliente.deamon = True
        thread_cliente.start()

    def escuchar(self):
        while True:
            time.sleep(0.001)
            data = self.cliente.recv(1024)
            print('La historia es: ' + data.decode('utf-8'))

    def enviar(self, data):
        self.cliente.send(data)




class Intefaz:
    def __init__(self):
        self.usuario = None
        self.cola_archivos = deque() # Guarda una lista con los nombres de los archivos

    def login(self):
        choice = input('S: servidor, C: cliente')
        if choice in ['s', 'S']:
            self.usuario = Servidor()
            print('Logeado como servidor')
        elif choice in ['c', 'C']:
            self.usuario = Cliente()
            print('Logeado como cliente')

    def mostrar_opciones(self):
        print('El programa cuenta con los siguientes comandos:\n'
              'mostrar \n'
              'agregar \n'
              'quitar \n'
              'enviar \n'
              'terminar \n'
              'help: muestra los comandos')

    def mostrar_por_enviar(self):
        print('Estos archivos se enviarán: ')
        for par in enumerate(self.cola_archivos):
            print('[{0}]: {1}'.format(*par))

    def agregar_archivo(self):
        lista = os.listdir('Archivos')
        for par in enumerate(lista):
            print('[{0}]: {1}'.format(*par))
        n = int(input('Selecciona el archivo que quieres agregar: '))
        try:
            self.cola_archivos.append(lista[n])
            print('Archivo agregado a la lista')
        except IndexError:
            print('Index Error')

    def enviar_archivos(self):
        print('Estos archivos se enviarán: \n')
        for file in self.cola_archivos:
            print(file)


        while self.cola_archivos:
            file = self.cola_archivos.popleft()
            with open('Archivos/' + file, 'rb') as file:
                self.usuario.enviar(file)





    def quitar_archivos(self):
        self.mostrar_por_enviar()
        n = int(input('Selecciona el archivo que quieres quitar de la lista: '))
        try:
            archivo = self.cola_archivos[n]
            self.cola_archivos.remove(archivo)
        except IndexError:
            print('Index Error')


    def run(self):
        self.login()
        self.mostrar_opciones()
        while True:
            comand = input('ingresa un comando$ ')
            if comand == 'mostrar':
                self.mostrar_por_enviar()
            elif comand == 'agregar':
                self.agregar_archivo()
            elif comand == 'quitar':
                self.quitar_archivos()
            elif comand == 'enviar':
                self.enviar_archivos()
            elif comand == 'help':
                self.mostrar_opciones()
            elif comand == 'terminar':
                print('Adios')
                return
            else:
                print('Comando invalido')




if __name__ == '__main__':


    interfaz = Intefaz()
    interfaz.run()