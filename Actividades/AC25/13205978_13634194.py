import socket
import threading
import time


class Cliente:
    def __init__(self, historia):
        self.historia = historia

        self.host = '127.0.0.1'
        self.port = 3505
        self.s_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.conectar()
            print('Hola')
        except socket.error:
            print('Chao')

    def conectar(self):
        self.s_cliente.connect((self.host, self.port))
        self.escuchador = threading.Thread(target=self.escuchar, args=())
        self.escuchador.deamon = True
        self.escuchador.start()

    def escuchar(self):
        while True:
            data = self.s_cliente.recv(1024)
            print('La historia es: ' + data.decode('utf-8'))

    def enviar(self, msj):
        self.s_cliente.send(msj.encode('utf-8'))

class Server:
    def __init__(self, historia):
        self.historia = historia

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


    def enviar(self, msj):
        self.cliente.send(msj.encode('utf-8'))


class Historia:
    def __init__(self):
        self.puede_jugar = True
        self.historial = []
        self.pierde = False

    def revisar(self, mensaje_enviado):
        for i in range(len(self.historial)):
            if mensaje_enviado[i] != self.historial[i]:
                self.pierde = True
                return


def str_to_list(mensaje):
    return mensaje.split(' ')


if __name__ == '__main__':

    click = input('S: Servidor, C: Cliente \n')

    if click == 'S' or click == 's':
        server = Server(Historia())
        server.aceptar()

        while True:
            if server.historia.puede_jugar:
                msj = input('Ingrese su historia de tres palabras:')
                server.enviar(msj)


    elif click == 'C' or click == 'c':

        client = Cliente(Historia())
        while True:
            if client.historia.puede_jugar:
                msj = input('Ingrese su historia de tres palabras:')
                client.enviar(msj)
