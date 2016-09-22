from PyQt4 import QtCore, QtGui, uic, QtWebKit
from collections import deque
from cliente import Cliente
from dropbox import files
import threading

main_window_ui = uic.loadUiType('mw.ui')


class Browser(QtGui.QWidget):
    def __init__(self, url):
        super().__init__()
        self.resize(700, 600)
        self.web_view = QtWebKit.QWebView(self)
        self.web_view.load(QtCore.QUrl(url))
        self.show()


class MainWindow(*main_window_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.cliente = Cliente()
        self.stackedWidget.setCurrentWidget(self.login_page)
        self.browser = Browser(self.cliente.authorize_url)

        self.pushButton.clicked.connect(self.acceder)
        self.subirButton.clicked.connect(self.actualizar)

        self.carpetas = []

    def acceder(self):
        if self.lineEdit.text():
            auth_code = self.lineEdit.text()
            if self.cliente.get_auth(auth_code):
                self.cambiar_a_dp_page()

            else:
                self.errorLabel.setText('Error, vuelve a intentarlo')

    def cambiar_a_dp_page(self):
        self.stackedWidget.setCurrentWidget(self.dp_page)

    def actualizar(self):
        item = QtGui.QTreeWidgetItem(['Hola'])

        sub_item = QtGui.QTreeWidgetItem(['Chao'])
        item.addChild(sub_item)
        self.treeWidget.addTopLevelItem(item)

    def setup_tree(self):

        carpetas = [entry.name for entry in self.cliente.dbx.files_list_folder('', recursive=False).entries]

        for item in carpetas:
            tree_item = QtGui.QTreeWidgetItem([item])
            self.treeWidget.addTopLevelItem(tree_item)
            self.agregar_hijo(tree_item, '/{}'.format(item))

    def agregar_hijo(self, tree_item, path):

        try:
            lista = self.cliente.dbx.files_list_folder(path, recursive=False).entries
        except Exception:
            print('Terminamos')
        else:
            for entry in lista:
                hijo_tree_item = QtGui.QTreeWidgetItem([entry.name])
                tree_item.addChild(hijo_tree_item)
                t = threading.Thread(target=self.agregar_hijo,
                                     args=(hijo_tree_item, path + '/{}'.format(entry.name)))
                t.setDaemon(True)
                t.start()



if __name__ == '__main__':
    app = QtGui.QApplication([])
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec_()
