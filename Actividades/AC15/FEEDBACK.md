### Distribución de puntajes

Requerimientos (**R**):

* **(0.5 pts)** R1: Revisar mean antes de var
* **(1.0 pts)** R2: Revisar que no haya worker ejecutando comando
* **(1.0 pts)** R3: Instanciar y echar a correr worker
* **(1.0 pts)** R4: Los workers que no han terminado se detienen al ingresar `exit`
* **(1.5 pts)** R5: Correcta ejecución de la función de cada worker
* **(1.0 pts)** R6: Se imprime cuáles workers terminaron su ejecución y cuáles no.

**Además, se descontará (0.2) puntos si no sigue formato de entrega.**

### Obtenido por el alumno
| R1 | R2 | R3 | R4 | R5 | R6 | Descuento |
|:---|:---|:---|:---|:---|:---|:----------|
| 0 | 0.5 | 1.0 | 0.5 | 0 | 0 | 0.4 |

| Nota |
|:-----|
| **2.6** |

### Comentarios

* El programa se cae con inputs incorrectos, además, pusiste setDaemon(True) antes de hacer super().__init__() en el __init__ de la clase worker, por lo que se produce un error
* No se controla que se calcule mean antes de var
* Se controla que no se hagan dos threada de lo mismo pero de manera incorrecta, ya que no se puede calcular lo mismo apun después de terminado el primer thread
* No se calcula nada
* No se imprimen los thread terminados ni los incompletos
