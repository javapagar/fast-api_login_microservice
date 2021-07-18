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

Instalo la librería fast-api y el servidor uvicorn, que será el encargado de manejar las peticiones a la API. Con este servidor la aplicación será completamente robusta en producción, lo que simplifica bastante la tarea.

        $ pip install fastapi uvicorn[standard]

Podemos ver todas las librerías instaladas con el comando

        $ pip freeze

y si queremos guardar las dependencias en el fichero requirements.txt

        $ pip freeze > requirements.txt

Ejecutaré el comando anterior siempre que hago un pip install en el entorno.

También, se instalará la librería SQLAlchemy, que es un ORM con el que gestionaremos la base de datos que complementará la aplicación.

        $ pip install SQLAlchemy


## Estructura del proyecto
En la raíz de la carpeta de la aplicación crearemos un archivo __init__.py vacío. Este archivo marcará la carpeta como un paquete python. En cada carpeta nueva que creemos dentro, también situaremos un archivo __init__.py, convirtiéndolo en un sub-paquete. DE igual manera, los archivos .py que se encuentren dentro de estas carpetas serán módulos o sub-módulos de python. De esta manera se podrá importar código de cualquier archivo a otro.

Para empezar crearemos la siguiente estructura

        .
        ├── app                  # es el paquete Python
        │   ├── __init__.py      # este fichero convierte a la carpeta "app" en un paquete Python
        │   ├── main.py          # Módulo "main"
        │   └── test             # "test" es un sub-paquete Python del paquete "app"
        │   │   ├── __init__.py  # convierte a la carpeta "test" en un sub-paquete Python
        │   │   ├── testapi.py   # Sub-módulo"testapi"

Como se comentó antes, los archivos init se dejarán vacíos. El módulo main será el encargado de crear la aplicación, y una primera prueba:

                from fastapi import FastAPI

                app = FastAPI()

                @app.get("/")
                async def root():
                return {"message": "Hello World"}

con estas líneas ya podríamos ejecutar el servicor uvicorn

                $ uvicorn main:app

y cuando esté levantado, podemos acceder a http://127.0.0.1:8000

Siguiendo con la prueba vamos a completar el módulo testapi. La anterior estructura sería la base de un proyecto grande, en el que cada subcarpeta nos ayudaría a tener más ordenado el código. EL archivo testapi contendrá el enrutamiento a otro recursos de la api que se deberá registrar en la aplicación principal. En Flask, esto se hacía a través de los Blueprints, en FastAPI se utilizará APIRouter. Vamos a ver un ejemplo con testapi:

                from fastapi import APIRouter

                router = APIRouter(prefix="/test",
                                tags=["test"])

                @router.get("/")
                async def root():
                return {"message": "Hello World from test"}

Con la clase APIRouter creamos un nuevo endpoint, con la propiedad prefix daremos la base de la url y con la propiedad tags definimos etiquetas que definirán las entradas en la documentación de la API.

Ahora, habrá que retocar el módulo main para registrar este nuevo enrutamiento:

                from fastapi import FastAPI
                from test import testapi

                app = FastAPI()
                app.include_router(testapi.router)

                @app.get("/")
                async def root():
                return {"message": "Hello World"}

Con estos sencillos pasos tendríamos disponible el endpoint http://127.0.0.1:8000/test

## Documentación de la API

Otra de las ventajas de usar FastAPI es que permite la construcción automática de la documentación de la API, aunque se puede hacer de diferentes maneras, dos están incluidas por defecto:

* Swagger UI http://127.0.0.1:8000/docs
* ReDoc http://127.0.0.1:8000/redoc
