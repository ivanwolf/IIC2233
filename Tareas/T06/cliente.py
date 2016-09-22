import time
import json
from PyQt4 import QtCore, QtGui, uic
from back_cliente import Cliente

login_window_ui = uic.loadUiType('gui/login.ui')
logged_window_ui = uic.loadUiType('gui/logged_window.ui')
new_user_ui = uic.loadUiType('gui/new_user.ui')
main_window_ui = uic.loadUiType('gui/main_window.ui')
add_friend_ui = uic.loadUiType('gui/add_friend.ui')
chat_window_ui = uic.loadUiType('gui/chat_window.ui')
archivos_window_ui = uic.loadUiType('gui/archivos_window.ui')
enviar_archivo_window_ui = uic.loadUiType('gui/enviar_archivo_window.ui')
aceptar_descargas_window_ui = uic.loadUiType('gui/aceptar_descargas_window.ui')


class MainWindow(*main_window_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cliente = Cliente(self)

        self.login_form = LoginForm(self)
        self.logged_window = None
        self.new_user_form = None
        self.chat_window = None
        self.agregar_amigo_form = None
        self.archivos_window = None
        self.enviar_archivo_window = None
        self.aceptar_descargas_window = None

        self.central_widget = QtGui.QStackedWidget()
        self.central_widget.addWidget(self.login_form)
        self.central_widget.setCurrentWidget(self.login_form)
        self.setCentralWidget(self.central_widget)

    def closeEvent(self, event):
        self.cliente.logout_req()

    def crear_cuenta_req(self):
        user_name = self.new_user_form.userlineEdit.text()
        password = self.new_user_form.passlineEdit.text()
        cpassword = self.new_user_form.cpasslineEdit.text()

        respuesta = self.cliente.crear_cuenta_req(user_name, password, cpassword)
        if respuesta[0]:
            self.cambiar_a_login_form()
        else:
            self.new_user_form.lable.setText(respuesta[1])

    def enviar_mp(self):
        if self.chat_window.listWidget.currentItem():
            msj = self.chat_window.textEdit.text()
            destinatario = self.chat_window.listWidget.currentItem().text()
            self.chat_window.textEdit.clear()

            if self.cliente.enviar_mp(msj, destinatario):
                self.chat_window.mostrar_chat()

    def login_req(self):
        user_name = self.login_form.userlineEdit.text()
        password = self.login_form.passlineEdit.text()
        respuesta = self.cliente.login_req(user_name, password)
        if respuesta[0]:
            self.cambiar_a_logged_window()
        else:
            self.login_form.label.setText(respuesta[1])

    def logout_req(self):
        self.cliente.logout_req()
        self.cambiar_a_login_form()

    def agregar_amigo_req(self):
        nombre_amigo = self.agregar_amigo_form.lineEdit.text()
        respuesta = self.cliente.add_friend_req(nombre_amigo)
        if respuesta[0]:
            self.cambiar_a_chat_window()
            self.agregar_amigo_form.cerrar()
        else:
            self.agregar_amigo_form.label.setText(respuesta[1])

    def mostrar_dialogo_amigo(self):
        self.agregar_amigo_form = NewFriendForm(self)
        self.agregar_amigo_form.show()

    def agregar_archivo(self):
        path = QtGui.QFileDialog.getOpenFileName(self)
        if self.cliente.agregar_archivo(path):
            self.archivos_window.setup_archivos()

    def agregar_carpeta(self):
        carpeta = QtGui.QFileDialog.getExistingDirectory(self)

        if self.cliente.agregar_carpeta(carpeta):
            pass
            # self.archivos_window.setup_carpetas()

    def actualizar(self):
        pass

    def cambiar_a_login_form(self):
        if self.login_form is None:
            self.login_form = LoginForm(self)
            self.central_widget.addWidget(self.login_form)
        self.setWindowTitle('Bienvenido a DropPox')
        self.central_widget.setCurrentWidget(self.login_form)

    def cambiar_a_new_user_form(self):
        if self.new_user_form is None:
            self.new_user_form = NewUserForm(self)
            self.central_widget.addWidget(self.new_user_form)
        self.setWindowTitle('Nuevo usuario')
        self.central_widget.setCurrentWidget(self.new_user_form)

    def cambiar_a_logged_window(self):
        if self.logged_window is None:
            self.logged_window = LoggedWindow(self)
            self.central_widget.addWidget(self.logged_window)
        self.setWindowTitle('Bienvenido')
        self.central_widget.setCurrentWidget(self.logged_window)

    def cambiar_a_chat_window(self):
        if self.chat_window is None:
            self.chat_window = ChatWindow(self)
            self.central_widget.addWidget(self.chat_window)
        self.setWindowTitle('Chat')
        self.chat_window.setup_amigos()
        self.chat_window.mensajesTextEdit.clear()
        self.chat_window.textEdit.clear()
        self.central_widget.setCurrentWidget(self.chat_window)

    def cambiar_a_archivos_window(self):
        if self.archivos_window is None:
            self.archivos_window = ArchivosWindow(self)
            self.central_widget.addWidget(self.archivos_window)
        self.setWindowTitle('Archivos')
        self.archivos_window.setup_archivos()
        self.central_widget.setCurrentWidget(self.archivos_window)

    def cambiar_a_enviar_archivo_window(self):
        if self.enviar_archivo_window is None:
            self.enviar_archivo_window = EnviarArchivoWindow(parent=self)
            self.central_widget.addWidget(self.enviar_archivo_window)

        self.setWindowTitle('Enviar archivo')
        self.enviar_archivo_window.setup_amigos()
        self.enviar_archivo_window.setup_archivos()
        self.central_widget.setCurrentWidget(self.enviar_archivo_window)

    def cambiar_a_aceptar_descargas_window(self):

        if self.aceptar_descargas_window is None:
            self.aceptar_descargas_window = AceptarDescargasWindow(parent=self)
            self.central_widget.addWidget(self.aceptar_descargas_window)
        self.setWindowTitle('Aceptar archivos')
        self.aceptar_descargas_window.setup_descargas()
        self.central_widget.setCurrentWidget(self.aceptar_descargas_window)


class NewFriendForm(*add_friend_ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.padre = parent
        self.exitButton.clicked.connect(self.cerrar)
        self.agregarButton.clicked.connect(self.padre.agregar_amigo_req)

    def cerrar(self):
        self.setParent(None)
        self.close()


class AceptarDescargasWindow(*aceptar_descargas_window_ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.padre = parent

        self.descargarButton.clicked.connect(self.descargar)
        self.rechazarButton.clicked.connect(self.rechazar_descarga)
        self.volverButton.clicked.connect(self.padre.cambiar_a_chat_window)

    def setup_descargas(self):
        self.descargaslistWidget.clear()
        descargas = self.padre.cliente.por_descargar()
        for _item in descargas:
            rep = '{}, {}'.format(_item[0], _item[1])
            item = QtGui.QListWidgetItem(rep)
            self.descargaslistWidget.addItem(item)

    def descargar(self):
        item = self.descargaslistWidget.currentItem()
        if item is not None:
            user_name, file_name = item.text().split(', ')
            path = QtGui.QFileDialog.getExistingDirectory(self)
            if self.padre.cliente.descargar_archivo(file_name, path, user_name=user_name):
                if self.padre.cliente.rechazar_descarga(user_name, file_name):
                    self.setup_descargas()

    def rechazar_descarga(self):
        item = self.descargaslistWidget.currentItem()
        if item is not None:
            user_name, file_name = item.text().split(', ')
            if self.padre.cliente.rechazar_descarga(user_name, file_name):
                self.setup_descargas()


class EnviarArchivoWindow(*enviar_archivo_window_ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.padre = parent

        self.volverButton.clicked.connect(self.padre.cambiar_a_chat_window)
        self.enviarButton.clicked.connect(self.enviar_archivo)

        self.setup_archivos()
        self.setup_amigos()

    def setup_archivos(self):
        self.archivoslistWidget.clear()
        lista_archivos = self.padre.cliente.lista_archivos()
        for archivo in lista_archivos:
            item = QtGui.QListWidgetItem(archivo)
            self.archivoslistWidget.addItem(item)

    def setup_amigos(self):
        self.amigoslistWidget.clear()
        lista_amigos = self.padre.cliente.lista_amigos()
        for amigo in lista_amigos:
            item = QtGui.QListWidgetItem(amigo)
            self.amigoslistWidget.addItem(item)

    def enviar_archivo(self):
        if self.archivoslistWidget.currentItem() and self.amigoslistWidget.currentItem():
            file_name = self.archivoslistWidget.currentItem().text()
            friend_name = self.amigoslistWidget.currentItem().text()
            if self.padre.cliente.enviar_archivo_mp(file_name, friend_name):
                self.padre.cambiar_a_chat_window()


class NewUserForm(*new_user_ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.padre = parent
        self.okButtom.clicked.connect(self.padre.crear_cuenta_req)
        self.backButtom.clicked.connect(self.padre.cambiar_a_login_form)


class LoginForm(*login_window_ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.padre = parent
        self.loginButtom.clicked.connect(self.padre.login_req)
        self.newuserButtom.clicked.connect(self.padre.cambiar_a_new_user_form)


class LoggedWindow(*logged_window_ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.padre = parent
        self.cliente = self.padre.cliente

        self.fileButton.clicked.connect(self.padre.cambiar_a_archivos_window)
        self.chatButton.clicked.connect(self.padre.cambiar_a_chat_window)
        self.logoutButton.clicked.connect(self.logout)

    def logout(self):
        self.padre.logout_req()


class ChatWindow(*chat_window_ui):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.padre = parent
        self.lista_amigos = self.padre.cliente.lista_amigos
        self.chats = {}
        self.amigos_escuchados = []

        self.agregarButton.clicked.connect(self.padre.mostrar_dialogo_amigo)
        self.volverButton.clicked.connect(self.padre.cambiar_a_logged_window)
        self.enviarButton.clicked.connect(self.padre.enviar_mp)
        self.archivoButton.clicked.connect(self.padre.cambiar_a_enviar_archivo_window)
        self.descargasButton.clicked.connect(self.padre.cambiar_a_aceptar_descargas_window)
        self.textEdit.returnPressed.connect(self.enviarButton.click)

        self.listWidget.itemClicked.connect(self.mostrar_chat)
        self.listWidget.itemClicked.connect(self.crear_worker)

    def setup_amigos(self):
        self.listWidget.clear()
        lista_amigos = self.padre.cliente.lista_amigos()
        for amigo in lista_amigos:
            item = QtGui.QListWidgetItem(amigo)
            self.listWidget.addItem(item)

    def crear_worker(self):
        amigo = self.listWidget.currentItem().text()
        if amigo not in self.amigos_escuchados:
            self.mensajesTextEdit.clear()
            self.amigos_escuchados.append(amigo)
            worker = Worker(amigo, parent=self)
            worker.start()

    def mostrar_chat(self):
        amigo = self.listWidget.currentItem().text()
        nuevo_chat = self.padre.cliente.get_chat(amigo)
        por_descargar = self.padre.cliente.por_descargar()
        if por_descargar:
            self.padre.cambiar_a_aceptar_descargas_window()

        if not self.mensajesTextEdit.toPlainText() or amigo not in self.chats:

            self.chats.update({amigo: nuevo_chat})
            for linea in nuevo_chat:
                rep = '{1} {0}: {2}'.format(*tuple(linea))
                self.mensajesTextEdit.append(rep)
            self.setWindowTitle(amigo)

        elif nuevo_chat != self.chats[amigo]:
            self.chats.update({amigo: nuevo_chat})
            self.mensajesTextEdit.clear()
            for linea in nuevo_chat:
                rep = '{1} {0}: {2}'.format(*tuple(linea))
                self.mensajesTextEdit.append(rep)
            self.setWindowTitle(amigo)


class ArchivosWindow(*archivos_window_ui):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.padre = parent

        self.agregarArchivoButton.clicked.connect(self.padre.agregar_archivo)
        self.agregarCarpetaButton.clicked.connect(self.padre.agregar_carpeta)
        self.descargarButton.clicked.connect(self.descargar)
        self.volverButton.clicked.connect(self.padre.cambiar_a_logged_window)
        self.actualizarButton.clicked.connect(self.padre.actualizar)

        path_carpetas = self.padre.cliente.path_carpetas()
        model = QtGui.QFileSystemModel()
        model.setRootPath(path_carpetas)

        self.treeView.setModel(model)
        self.treeView.setRootIndex(model.index(path_carpetas))

    def setup_archivos(self):
        self.archivoslistWidget.clear()
        lista_archivos = self.padre.cliente.lista_archivos()
        for archivo in lista_archivos:
            item = QtGui.QListWidgetItem(archivo)
            self.archivoslistWidget.addItem(item)

    def descargar(self):
        path = QtGui.QFileDialog.getExistingDirectory(self)
        file_name = self.archivoslistWidget.currentItem().text()
        if self.padre.cliente.descargar_archivo(file_name, path):
            pass


class Worker(QtCore.QThread):
    signal = QtCore.pyqtSignal()

    def __init__(self, friend_name, parent=None):
        super().__init__(parent)
        self.padre = parent
        self.friend_name = friend_name
        self.signal.connect(self.padre.mostrar_chat)

    def run(self):
        chat_actual = self.friend_name
        while chat_actual == self.friend_name and (
                    self.padre == self.padre.padre.central_widget.currentWidget()):
            time.sleep(0.8)
            self.signal.emit()
            chat_actual = self.padre.listWidget.currentItem().text()
        self.padre.amigos_escuchados.remove(self.friend_name)


if __name__ == '__main__':
    app = QtGui.QApplication([])
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec_()
