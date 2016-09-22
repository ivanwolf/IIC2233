## Bienvenido a pseudo Battleship de Bummer UC

#### Acerca del juego
 Ejecutar ```main.py``` y seguir las instrucciones que indique la consola.
 Los el daño que hacen los ataque ha sido aumentado en 10 puntos, esto es para mejorar la jugabilidad, ya que si no, el juego se hace muy lento.

 Estan habilitados todos ataques y movimientos, manejando la disponibilidad.

#### Manejo de excepciones:
Si bien el formato de los inputs está especificado, el programa maneja las excepciones y no se caerá en caso de ingresar algún string no válido.

#### Acerca de la inteligencia:
Existe la posibilidad de jugar contra la computadora, pero solo en un tablero de 8x8, esto es por que el algortimo es un poco exhaustivo y si el tablero es muy grande se demoraría mucho en pensar.

El computador solo usa el Ataque Normal y funciona como un Battleship comun y corriente, no usa otros ataques y "asume" que el jugador real no mueve sus barcos. Si nos basamos en estas hipótesis la computadora probablemente nos gane.

#### Acerca de los test
La mayoria de las funciones que ameritaban ser testeadas fueron testeadas con la librería ```unittest```. En mi código hay funciones que consideré que no debían ser testeadas ya que son parte de la funcionabilidad del programa (o algo así), por ejemplo, el método ```turno``` de la clase ```Partida``` es la funcion principal del programa que hace que el jugador pueda hacer todo. Otras funciones solo "calculan" algo, y si las testeara solo estaría testeando las funciones ```built-in``` de python. El resto de las funciones estan testeadas en los archivos que comienzan con test.
