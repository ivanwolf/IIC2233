import json
import os


class BaseUsuarios:
    def __init__(self, path):
        """
        Esta clase manejara la lista con los diccionarios que representan a cada ususario
        de DropPox
        :param path: direccion de la carpeta donde se encuentra la información
        """
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        self.lista_usuarios = []
        for user in os.listdir(self.path):
            self.lista_usuarios.append(user[:-4])

    def crear_usuario(self, user_name, password):
        user = {'user_name': user_name,
                'pass': password,
                'logged': False,
                'amigos': [],
                'enviados': [],
                'recibidos': [],
                'descargar': []
                }

        with open(self.path + '/{0}.txt'.format(user_name), 'w') as file:
            json.dump(user, file, indent=4)
        self.lista_usuarios.append(user_name)

    def get_usuario(self, user_name):

        with open(self.path + '/{0}.txt'.format(user_name), 'r') as file:
            user = json.load(file)
        return user

    def existe_usuario(self, user_name):
        if '{}.txt'.format(user_name) in os.listdir(self.path):
            return True
        return False

    def write(self, user_name, key, value):
        user = self.get_usuario(user_name)
        user.update({key: value})

        with open(self.path + '/{0}.txt'.format(user_name), 'w') as file:
            json.dump(user, file, indent=4)


class BaseArchivos:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        self.lista_usuarios = []
        for user in os.listdir(self.path):
            self.lista_usuarios.append(user)

    def crear_carpeta_usuario(self, user_name):
        path = self.path + '/' + user_name
        if not os.path.exists(path):
            os.makedirs(path)
            os.makedirs(path + '/' + 'archivos')
            os.makedirs(path + '/' + 'carpetas')

    def get_archivo(self, user_name, file_name):
        path = '{}/{}/{}/{}'.format(self.path, user_name, 'archivos', file_name)
        with open(path, 'rb') as file:
            bites = file.read()
        return bites

    def get_lista_archivos(self, user_name):
        path = '{}/{}/{}'.format(self.path, user_name, 'archivos')
        return os.listdir(path)

    def get_path_carpetas(self, user_name):
        return '{}/{}/{}'.format(self.path, user_name, 'carpetas')

    def guardar_archivo(self, user_name, file_name, bites):

        path = '{}/{}/{}/{}'.format(self.path, user_name, 'archivos', file_name)
        with open(path, 'wb') as file:
            file.write(bites)

    def guardar_carpeta(self, user_name, dir_name, archivos):
        # archivos es un dic, donde la llave es el nombre del archivo y el value
        # son los bites
        path = '{}/{}/{}/{}'.format(self.path, user_name, 'carpetas', dir_name)
        os.makedirs(path)
        for (file_name, bites) in archivos.items():
            with open('{}/{}'.format(path, file_name), 'wb') as file:
                file.write(bites)
