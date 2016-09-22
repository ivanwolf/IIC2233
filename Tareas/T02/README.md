## Bienvenido a la red de Bummer UC

> #### Instrucciones

>-  Correr el archivo ```main.py``` , esto se demorará un par de segundos (minutos) ya que se comenzará a recorred la red. Luego sel tiempo de carga se generarán los archivos```red.txt```,  ```rutaABummer.txt```,  ```rutasDobleSentido.txt``` y ```test.txt```. El ultimo archivo sólo es de prueba y sirve para poder conocer el estado de los puertos. Todos los archivos son guardados en la carpeta ```data``` que se creará en la misma direccion en la que se encuentre el archivo ```main.py```.

> #### Acerca de las EDD:

>-  ``` class Lista``` 
>Es la clase de que se trata de parecer lo más posible a la clase ```list```, como base se utilizo el ejemplo de listas ligadas visto en el curso.  Muchas de las funciones mágicas están disponibles para la clase ```Lista```.
>- ```class Dict```
>A partir de la clase ```Lista``` cree esta clase que es un diccionario pero menos poderoso. Se trata de una tabla de hash y la función de hash es aplicar ```%``` a la llave, por esa razón, las llaves de este diccionario sólo pueden ser enteros. La idea detrás es guardar una lista con ```n``` entradas, donde cada entrada contiene a su vez otra lista, la cual está vacía al principio.  Luego para guardar ```value ``` con la llave ```m```, guardamos la tupla ```(m, value)``` en la lista de la casilla ```m % n``` . De esa forma para poder acceder al objeto buscado se hace más fácil que tener que iterar sobre toda una lista. Para más información revisar el archivo ```estructuras.py```.
>- ```class Tupla```
> A partir de la clase ```Lista``` cree esta clase, es similar a la clase ```tuple``` pero con menos métodos.
 
> #### Acerca de los algortimos:
>- No está demás decir que los algoritmos utilizados no son invención mía, sino  son el fruto del arduo estudio de la teoría de grafos. La cuál es un área de la matemática muy interesante y aplicable.

 Written with [StackEdit](https://stackedit.io/).
