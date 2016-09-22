import socket
import threading
import hashlib
import pickle
from datetime import datetime
from data_base import BaseUsuarios, BaseArchivos

HOST = '127.0.0.1'
PORT = 3492
NUM = 10


class Server:
    def __init__(self):

        self.host = HOST
        self.port = PORT

        self.s_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_server.bind((self.host, self.port))
        self.s_server.listen(NUM)

        self.dict_clientes = {}
        self.base_usuarios = BaseUsuarios('db/users')
        self.base_archivos = BaseArchivos('db/files')
        self.connection = True

        thread_aceptar = threading.Thread(target=self.aceptar, args=())
        thread_aceptar.setDaemon(True)
        thread_aceptar.start()

        print('Bienvenido al Servidor de DropPox')

    def aceptar(self):
        while True:
            # Aca estamos guardadno el socket del cliente nuevo
            cliente_nuevo, addres = self.s_server.accept()

            thread_cliente = threading.Thread(target=self.escuchar_cliente, args=(cliente_nuevo,))
            thread_cliente.daemon = True
            thread_cliente.start()

    def desconectar(self):
        for user_name in self.dict_clientes:
            self.base_usuarios.write(user_name, 'logged', False)
        self.connection = False
        self.s_server.close()

    def escuchar_cliente(self, cliente):
        """
        Los mensajes que el cliente le envie al servidor seran tuplas, donde la primera
        componente representará la función que el servidor debe ejecutar y la segunda será
        otra tupla con los argumentos de la función.
        """
        while self.connection:
            try:
                largo = int(cliente.recv(16).decode('utf-8'))
                data = bytes()
                for i in range((largo // 1024) + 1):
                    data += cliente.recv(1024)
                self.process_data(cliente, data)

            except (EOFError, ValueError):
                return

    def crear_usuario(self, cliente, user_name, password, confirm_password):
        """
        Debemos comprobar si es que el usuario ya existe, luego revisar que las claves
        coincidan y finalmente agregar el usuario a la base con la clave hasheada
        """
        if self.base_usuarios.existe_usuario(user_name):
            self._enviar(cliente, False, 'Nombre de usuario no disponible, vuelve a intentarlo')

        elif password != confirm_password:
            self._enviar(cliente, False, 'Las claves no coinciden, vuelve a intentarlo')

        else:
            hash_password = hashlib.sha1(password.encode()).hexdigest()
            try:
                self.base_usuarios.crear_usuario(user_name, hash_password)
                self.base_archivos.crear_carpeta_usuario(user_name)
            except Exception:
                print('[SERVER]: Error, no se pudo crear el usuario')
            else:
                self._enviar(cliente, True, 'Usuario creado con éxito')
                print('[SERVER]: Usuario {} creado correctamente'.format(user_name))

    def log_in(self, cliente, user_name, password):

        if not self.base_usuarios.existe_usuario(user_name):
            self._enviar(cliente, False, 'Error, el usuario no existe')
            return

        hash_password = hashlib.sha1(password.encode('utf-8')).hexdigest()
        user = self.base_usuarios.get_usuario(user_name)

        if user['logged']:
            self._enviar(cliente, False, 'Error, el usuario ya está conectado')
            return

        if hash_password == user['pass']:
            self.base_usuarios.write(user_name, 'logged', True)
            self._enviar(cliente, True, 'Usuario conectado correctamente', user_name)
            self.dict_clientes.update({user_name: cliente})

            print('[SERVER]: Usuario {} logeado correctamente'.format(user_name))

        else:
            self._enviar(cliente, False, 'Error, clave incorrecta')

    def add_friend(self, cliente, user_name, friend_name):
        if not self.base_usuarios.existe_usuario(friend_name):
            self._enviar(cliente, False, 'Error, el usuario no existe')
            return

        user = self.base_usuarios.get_usuario(user_name)
        amigos = user['amigos']
        if friend_name in amigos or friend_name == user_name:
            self._enviar(cliente, False, 'Error, el usuario ya es tu amigo')
        else:
            amigos.append(friend_name)
            self.base_usuarios.write(user_name, 'amigos', amigos)
            self._enviar(cliente, True,
                         'Usuario {} agregado a tu lista de amigos'.format(friend_name))

    def get_chat(self, cliente, user_name, friend_name):
        user = self.base_usuarios.get_usuario(user_name)
        enviados = user['enviados']
        recibidos = user['recibidos']
        lista = []
        for tupla in enviados:
            if tupla[0] == friend_name:
                tupla[0] = user_name
                lista.append(tupla)

        f_recibidos = [tupla for tupla in recibidos if tupla[0] == friend_name]
        lista = lista + f_recibidos
        lista.sort(key=lambda x: x[1])
        bites = pickle.dumps(lista)
        largo = str(len(bites)).zfill(16).encode('utf-8')
        cliente.send(largo + bites)

    def get_lista_amigos(self, cliente, user_name):
        user = self.base_usuarios.get_usuario(user_name)
        self._enviar(cliente, user['amigos'])

    def get_lista_archivos(self, cliente, user_name):
        lista = self.base_archivos.get_lista_archivos(user_name)
        self._enviar(cliente, lista)

    def get_path_carpetas(self, cliente, user_name):
        path = self.base_archivos.get_path_carpetas(user_name)
        self._enviar(cliente, path)

    def get_por_descargar(self, cliente, user_name):
        user = self.base_usuarios.get_usuario(user_name)
        self._enviar(cliente, user['descargar'])

    def enviar_archivo(self, cliente, user_name, file_name):
        bites = self.base_archivos.get_archivo(user_name, file_name)
        largo = str(len(bites)).zfill(16).encode('utf-8')
        cliente.send(largo + bites)

    def log_out(self, cliente, user_name):
        try:
            del self.dict_clientes[user_name]
        except KeyError:
            pass
        else:
            self.base_usuarios.write(user_name, 'logged', False)
            print('[SERVER]: Usuario {} desconectado correctamente'.format(user_name))

    def mensaje_privado(self, cliente, emisor, mensaje, destinatario):
        fecha = datetime.now().date()
        hora = str(datetime.now().time())[:8]
        time = '{} - {}'.format(fecha, hora)

        emisor_user = self.base_usuarios.get_usuario(emisor)
        mensajes_enviados = emisor_user['enviados']
        mensajes_enviados.append((destinatario, time, mensaje))

        destin_user = self.base_usuarios.get_usuario(destinatario)
        mensajes_recibidos = destin_user['recibidos']
        mensajes_recibidos.append((emisor, time, mensaje))

        self.base_usuarios.write(emisor, 'enviados', mensajes_enviados)
        self.base_usuarios.write(destinatario, 'recibidos', mensajes_recibidos)

        self._enviar(cliente, True)

    def mensaje_privado_archivo(self, cliente, user_name, file_name, friend_name):
        destin_user = self.base_usuarios.get_usuario(friend_name)
        por_descargar = destin_user['descargar']
        por_descargar.append((user_name, file_name))
        self.base_usuarios.write(friend_name, 'descargar', por_descargar)
        self._enviar(cliente, True)

    def rechazar_descarga(self, cliente, usuario, usuario_e, file_name):
        user = self.base_usuarios.get_usuario(usuario)
        por_descargar = user['descargar']
        por_descargar.remove([usuario_e, file_name])
        self.base_usuarios.write(usuario, 'descargar', por_descargar)
        self._enviar(cliente, True)

    def guardar_archivo(self, cliente, user_name, file_name, bites):
        self.base_archivos.guardar_archivo(user_name, file_name, bites)
        self._enviar(cliente, True)

    def guardar_carpeta(self, cliente, user_name, dir_name, archivos):
        self.base_archivos.guardar_carpeta(user_name, dir_name, archivos)
        self._enviar(cliente, True)

    def process_data(self, cliente, data):
        accion, args = pickle.loads(data)
        if accion == 'N':  # N de nuevo
            self.crear_usuario(cliente, *args)
        if accion == 'L':  # L de Log in
            self.log_in(cliente, *args)
        if accion == 'Q':  # Q de quit
            self.log_out(cliente, args)
        if accion == 'FL':
            self.get_lista_amigos(cliente, args)
        if accion == 'MP':  # Mensaje personal
            self.mensaje_privado(cliente, *args)
        if accion == 'PD':
            self.get_por_descargar(cliente, args)
        if accion == 'MPA':
            self.mensaje_privado_archivo(cliente, *args)
        if accion == 'RD':
            self.rechazar_descarga(cliente, *args)
        if accion == 'A':
            self.add_friend(cliente, *args)
        if accion == 'GC':
            self.get_chat(cliente, *args)
        if accion == 'File':
            self.guardar_archivo(cliente, *args)
        if accion == 'Dir':
            self.guardar_carpeta(cliente, *args)
        if accion == 'LA':
            self.get_lista_archivos(cliente, args)
        if accion == 'D':
            self.enviar_archivo(cliente, *args)
        if accion == 'PA':
            self.get_path_carpetas(cliente, args)

    def _enviar(self, cliente, *args):
        data = pickle.dumps(args)
        cliente.send(data)


if __name__ == '__main__':
    servidor = Server()
    while servidor.connection:
        command = input('Para salir del servidor ingrese -q')
        if command == '-q':
            servidor.desconectar()

    print('Adios!')
