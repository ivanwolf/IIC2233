from dropbox import Dropbox, files, DropboxOAuth2FlowNoRedirect
from tree import Nodo, Tree
import threading




APP_KEY = 'zzu98rrak12exhg'
APP_SECRET = 'pqjtoyxcpetwy4q'

class Cliente:

    def __init__(self):

        self.auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
        self.authorize_url = self.auth_flow.start()

        self.dbx = None
        self.tree = Tree()

        self.path_actual = '' # Si el string es vacío estamos en el root


    def get_auth(self, auth_code):
        try:
            access_token, user_id = self.auth_flow.finish(auth_code)
        except Exception as e:
            print('Error: %s' % (e,))
            return False
        else:
            self.dbx = Dropbox(access_token)
            self.setup_tree(self.tree.root, '')
            return True

    def setup_tree(self, nodo_actual, path):

        print(threading.current_thread().name)
        lista = self.dbx.files_list_folder(path, recursive=False).entries
        for entry in lista:
            nodo = Nodo(entry.name, entry)
            self.tree.agregar_nodo(nodo_padre=nodo_actual, nodo_hijo=nodo)
            if isinstance(entry, files.FolderMetadata):
                t = threading.Thread(name=entry.name ,target=self.setup_tree, args=(nodo, entry.path_lower))
                t.setDaemon(True)
                t.start()


