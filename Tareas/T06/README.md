## Bienvenido a DropPox F.A.Q

### ¿Cómo ingreso a DropPox?
Dentro de este repo encontraras 4 scripts escritos en ```python3```.
Si eres un cliente sólo debes correr ```cliente.py```. Debo mencionar que solo podrás ingresar si es que el servidor está disponible. El cliente tiene una interfaz gráfica decente.

Si eres el servidor debes ejecutar ```server.py```. La interfaz del servidor es por comando. Si es que quieres cerrar el servidor y desconectar a todos los usuarios usar ```-q```.

### ¿Qué puedo hacer en DropPox si soy cliente?

DropPox esta en su fase alpha por lo tanto no todas las caracteriticas están habilitadas. Sin embargo, te podemos ofrecer:

- Crear usuario
- Agregar amigos
- Chatear en vivo con tus amigos
- Subir Archivos
- Subir Carpetas
- Descargar Archivos
- Enviar archivos a algún amigo
- Aceptar o rechazar Archivos

### ¿Existe alguna restricción de lo que puedo hacer?

Sí. Nuestro servidor supone que las carpetas que vas a subir no contienen otras carpetas en su interior.

### ¿Cómo guarda la información el servidor?

El servidor crea una carpeta llamada ```db``` ahí habran otras dos, ```user```
y ```files```. En La carpeta ```user``` se guarda, por cada usuario, un documento de texto plano con un objeto en formato ```json``` con la informacion de cada cuenta. (Tranquilo, tu clave no aparecerá). En la carpta ```files``` habra una carpeta por cada usuario registrado en el sistema donde se guardaran tus archivos.

### ¿Qué hago si el cliente no responde?

No está comprobado que el programa este libre de bugs, trate de capturar la mayor cantidad de excepciones, pero quizás me falte más de alguna. Si surge un problema cierra el cliente y vuelve a entrar. Si después el servidor no te deja entrar, debes terminar la ejecución de ```server.py``` y voler a correr el script.

### ¿Qué dependencias tiene el cliente?

El script del cliente debe estar en la misma dirección que la carpeta ```gui``` que contiene las dependencias necesarias para la interfaz gráfica.
