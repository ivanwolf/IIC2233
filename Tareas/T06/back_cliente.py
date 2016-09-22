import socket
import sys
import pickle
import os

HOST = '127.0.0.1'
PORT = 3492


class Cliente:
    def __init__(self, gui):
        self.host = HOST
        self.port = PORT
        self.gui = gui
        self.s_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connection = True
        self.user_name = None
        self.llego_algo = False

        try:
            self.s_cliente.connect((self.host, self.port))
        except socket.error:
            print("No fue posible realizar la conexión")
            sys.exit()

    def desconectar(self):
        self.connection = False

    def _enviar(self, accion, argumentos):
        data = pickle.dumps((accion, argumentos))
        largo = str(len(data)).zfill(16).encode('utf-8')
        self.s_cliente.send(largo + data)

    def crear_cuenta_req(self, user_name, password, c_password):
        self._enviar('N', (user_name, password, c_password))
        return self.s_cliente.recv(1024)

    def login_req(self, user_name, password):
        self._enviar('L', (user_name, password))
        respuesta = pickle.loads(self.s_cliente.recv(1024))
        if respuesta[0]:
            self.user_name = respuesta[2]
        return respuesta

    def add_friend_req(self, friend_name):
        self._enviar('A', (self.user_name, friend_name))
        return pickle.loads(self.s_cliente.recv(1024))

    def logout_req(self):
        self._enviar('Q', self.user_name)  # Con esto le decimos al servidor que nos borre

    def lista_amigos(self):
        self._enviar('FL', self.user_name)
        return pickle.loads(self.s_cliente.recv(1024))[0]

    def lista_archivos(self):
        self._enviar('LA', self.user_name)
        return pickle.loads(self.s_cliente.recv(1024))[0]

    def path_carpetas(self):
        self._enviar('PA', self.user_name)
        return pickle.loads(self.s_cliente.recv(1024))[0]

    def por_descargar(self):
        self._enviar('PD', self.user_name)
        return pickle.loads(self.s_cliente.recv(1024))[0]

    def get_chat(self, friend_name):
        self._enviar('GC', (self.user_name, friend_name))
        data = bytes()
        largo = int(self.s_cliente.recv(16).decode('utf-8'))
        for i in range((largo // 1024) + 1):
            data += self.s_cliente.recv(1024)
        return pickle.loads(data)

    def agregar_carpeta(self, carpeta):

        if os.path.isdir(carpeta):
            dir_name = carpeta.split('/')[-1]
            archivos = {}
            for file_name in os.listdir(carpeta):
                camino = '{}/{}'.format(carpeta, file_name)
                with open(camino, 'rb') as file:
                    archivos.update({file_name: file.read()})
            self._enviar('Dir', (self.user_name, dir_name, archivos))

    def agregar_archivo(self, path):
        file_name = path.split('/')[-1]
        with open(path, 'rb') as file:
            bites = file.read()
        self._enviar('File', (self.user_name, file_name, bites))
        return pickle.loads(self.s_cliente.recv(1024))[0]

    def rechazar_descarga(self, user_name, file_name):
        self._enviar('RD', (self.user_name, user_name, file_name))
        return pickle.loads(self.s_cliente.recv(1024))[0]

    def descargar_archivo(self, file_name, path, user_name=None):
        if user_name is None:
            user_name = self.user_name
        self._enviar('D', (user_name, file_name))
        data = bytes()
        largo = int(self.s_cliente.recv(16).decode('utf-8'))
        for i in range((largo // 1024) + 1):
            data += self.s_cliente.recv(1024)
        with open('{}/{}'.format(path, file_name), 'wb') as file:
            file.write(data)
        return True

    def quit_req(self):
        self._enviar('Q', self.user_name)

    def enviar_archivo_mp(self, file_name, friend_name):
        self._enviar('MPA', (self.user_name, file_name, friend_name))
        return pickle.loads(self.s_cliente.recv(1024))[0]

    def enviar_mp(self, msj, destinatario):
        self._enviar('MP', (self.user_name, msj, destinatario))
        return pickle.loads(self.s_cliente.recv(1024))[0]
