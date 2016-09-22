### Distribución de puntajes

Requerimientos (**R**):

* **(3.0 pts)** R1: Se manejan todos los errores que generan la falla del sistema
* **(3.0 pts)** R2: Se notifica qué no se pudo hacer y la razón del error

**Se descontará (1.5) puntos por cada error que no se maneje (0.75 por no manejo y 0.75 por no notificación del error).**

### Obtenido por el alumno
| R1 | R2 | R3 | R4 | R5 | R6 | Descuento |
|:---|:---|:---|:---|:---|:---|:----------|
| 3 | 2.3 | 0 | 0 | 0 | 0 | 0 |

| Nota |
|:-----|
| **7.0** |

(tus puntajes no coinciden porque tu pareja subió una mejor, si vuelven a subir los 2 la actividad, pondré la peor nota porque haces perder tiempo!)

### Comentarios
Buena actividad!! Te recomiendo para capturar el nombre del tipo de excepción usar:

except Exception as err:
    print("[ERROR]", type(err).__name__)

y en la segunda parte te baje un poquito porque se te fue poner en algunos casos que cosa no se pudo realizar!

por ejemplo pusiste:

ValueError
La nota debe ser entera (int) y no un string

pero falto agregar que no se pudo calificar al alumno!

saludos!

