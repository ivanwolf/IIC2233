from utils.parser import ApacheLogsParser


class BigAnalizador:
    def __init__(self, logs):
        self.logs = logs

    def bytes_transferidos(self):
        # Completar
        pass

    def errores_servidor(self):
        lista_status = list(map(obtener_status, self.logs))
        status_malos = list(filter(not_exitosa, lista_status))
        n = list(enumerate(status_malos))[-1][0]
        print('Solicitudes erroneas: {}\n'.format(n))

    def solicitudes_exitosas(self):
        lista_status = list(map(obtener_status, self.logs))
        status_buenos = list(filter(exitosa, lista_status))
        n = list(enumerate(status_buenos))[-1][0]

        print('Solicitudes exitosas: {}\n'.format(n))

    def url_mas_solicitada(self):
        # Completar
        pass


def exitosa(status):
    if status == 200 or status == 302 or status == 304:
        return True
    elif status == 404 or status == 500 or status == 501:
        return False


def not_exitosa(status):
    if status == 200 or status == 302 or status == 304:
        return False
    elif status == 404 or status == 500 or status == 501:
        return True


def obtener_status(self):
    return self.status


if __name__ == '__main__':
    parser = ApacheLogsParser("./utils/nasa_logs_week.txt")
    logs = parser.get_apache_logs()
    biganalizador = BigAnalizador(logs)  # Lista de logs

    biganalizador.bytes_transferidos()
    biganalizador.errores_servidor()
    biganalizador.solicitudes_exitosas()
    biganalizador.url_mas_solicitada()
