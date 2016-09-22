import threading
import datetime


class Worker(threading.Thread):
    instances = list()
    mean_data = dict()
    loaded_stars = dict()
    outputs = []

    lock = threading.Lock()

    def __init__(self, star_name, function_name):
        super().__init__()
        self.star_name = star_name
        self.nombre_funcion = function_name
        self.function = Worker.functions(function_name)
        self.command = "{} {}".format(function_name, star_name)
        print("Creando Worker para: {}".format(self.command))
        self.setDaemon(True)
        Worker.instances.append(self)

    @staticmethod
    def functions(func_name):
        def open(star_name):
            with __builtins__.open(star_name, 'r+') as file:
                lines = file.readlines()
                Worker.loaded_stars.update({star_name: lines})
            return 'DONE'

        def mean(star_name):
            datos = Worker.mean_data[star_name]
            ans = sum(map(lambda l: float(l), datos)) / len(datos)
            Worker.mean_data.update({star_name: ans})
            return ans

        def var(star_name):
            lines = Worker.loaded_stars[star_name]
            prom = Worker.mean_data[star_name]
            n = len(lines)
            suma = sum(map(lambda l: (float(l) - prom) ** 2, lines))
            return suma / (n - 1)

        return locals()[func_name]


def run(self):
    tupla = (self.getName(), self.command, self.function(self.star_name), datetime.datetime.now())
    with Worker.lock:
        Worker.outputs.append(tupla)


if __name__ == "__main__":
    output_list = list()  # variables agregadas
    loaded_stars = dict()  # para esta actividad
    command = input("Ingrese siguiente comando:\n")

    while command != "exit":
        # Preocupate del comando "status"

        try:
            function, starname = command.split(" ")

            executed = False
            for w in Worker.instances:
                if w.command == command and w.isAlive():
                    print("[DENIED] Ya hay un worker ejecutando el comando")
                    executed = True
                    break

            if not executed:
                # preocupate de que solo se cree un worker
                # si la estrella ya fue cargada
                # al diccionario
                if function == "var" and starname not in Worker.mean_data:
                    print("[DENIED] No se puede calcular varianza "
                          "sin haber calculado el promedio antes!")

                elif starname in ["AlphaCentauri", "Arcturus",
                                  "Canopus", "Sirius", "Vega"]:
                    Worker(starname, function).start()

                else:
                    print("[DENIED] Comando invalido\n\t"
                          "El nombre de la estrella no es correcto")

        except (ValueError, KeyError) as err:
            print("[DENIED] {}\n\tComando invalido".format(type(err).__name__))

        command = input("Ingrese siguiente comando:\n")

    # Reemplazar esto por imprimir lista de outputs
    # y luego, imprimir los que aun no han terminado
    print("Comandos ingresados por el usuario:")
    for w in Worker.instances:
        string = "NO alcanzo a terminar: " if w.isAlive() \
            else "Alcanzo a terminar: "
        print(string + w.command)

    print('Lista de outputs')
    for out in Worker.outputs:
        print(out)