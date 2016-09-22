from interfaz import Interfaz
from parsing import obtener_datos
import time

now = time.time()
### Si los archivos no estan en la carpeta data, por favor especificar el path
dic_personas = obtener_datos('data/personas.txt')
dic_cursos = obtener_datos('data/cursos.txt')
dic_evaluaciones = obtener_datos('data/evaluaciones.txt')
dic_requisitos = obtener_datos('data/requisitos.txt')

bummer = Interfaz()
bummer.instanciar_personas(dic_personas)
bummer.instanciar_cursos(dic_cursos, dic_requisitos, dic_evaluaciones)

print('Tiempo en cargar: {} seg'.format(str(time.time() - now)))

bummer.set_time()
bummer.correr()
