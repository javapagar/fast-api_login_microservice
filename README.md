# fast-api_login_microservice

https://realpython.com/fastapi-python-web-apis/

## Stack
SO Mac OS 10.13.6
Python 3.9.6


## Preparando el entorno
Lo primero, será crear un entorno virtual dentro de la carpeta de la aplicación, para poder instalar las librerías necesarias.

        $ python3 -m venv venv

Se activa el entorno

        $ source venv/bin/activate

Instalo la libreria fast-api y el servidor uvicorn, que será el encargado de manejar las peticiones a la API. Con este servidor la aplicación será completamente robusta en producción, lo que simplifica bastante la tarea.

        $ pip install fastapi uvicorn[standard]

Podemos ver todas las librerias instaladas con el comando

        $ pip freeze

y si queremos guardar las dependencias en el fichero requirements.txt

        $ pip freeze > requirements.txt

Ejecutaré el comando anterior siempre que hago un pip install en el entorno.

Tambiel instalaré la librería SQLAlchemy, que es un ORM con el que gestionaré la base de datos que complementará la aplicación.

        $ pip install SQLAlchemy

