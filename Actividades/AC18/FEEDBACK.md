### Distribución de puntajes

Requerimientos (**R**):

* **(3.0 pts)** R1: El programa imprime registro de todos los eventos que ocurren.
* **(1.0 pts)** R2: Paciencia de los clientes, se van despues de un cierto tiempo de espera.
* **(1.0 pts)** R3: Los clientes llamados por celular se van sin terminar.
* **(1.0 pts)** R4: Crea un main parametrizable.

**Además, se descontará (0.2) puntos si no sigue formato de entrega.**

### Obtenido por el alumno
| R1 | R2 | R3 | R4 |Descuento |
|:---|:---|:---|:---|:----------|
| 1.5 | 0 | 0.5  | 0.3|  0|

| Nota |
|:-----|
| 3.3 |

### Comentarios

Falta escribir cuando cliente se va.
Hay errores, cliente recibe llamado una vez que se sienta.
Se puede ir antes de ser atendido cuando se aburre.
main
Falta terminarlo! Debías poner
    env = simpy.Environment()
    res = Restaurante(env, TABLES)
    env.process(generador_clientes(env, INTERVAL, res))
    env.run(until=SIM_TIME)
pass va solo si no escribes nada en el método. 

* Sin Comentarios
