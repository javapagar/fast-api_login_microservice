# fast-api_login_microservice

https://realpython.com/fastapi-python-web-apis/

## Stack
SO Mac OS 10.13.6
Python 3.9.6
Docker 20.10.7


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
        ├── login-service
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


## Docker

Desde 2013, este proyecto open source y sus herramientas comienzan a ganar popularidad entre los desarrolladores, ya que suponía una solución mucho más ligera a la creación de máquinas virtuales, sustituyéndolas por el uso de contenedores. Cada contenedor es capaz de albergar una aplicación y todas sus dependencias y librerías, sin necesidad de un SO, cosa a la que estas obligado, si vas a utilizar una máquina virtual. De esta forma, los desarrolladores son capaces de crear en local, de forma fácil y sencilla, un entorno idéntico al que se utilizará en producción.

Resumiendo mucho, Docker permite, a través de un fichero de configuración y el código de la aplicación, construir una imagen que puede ser implementada a través de un contenedor en cualquier máquina de forma rápida y sencilla, y que permite una capa de abstracción total sobre la tecnología que necesita la aplicación, ya que el fichero se encargará de esto.

## Crear Dockerfile, el fichero de configuración
En este momento nuestra aplicación consta de un único micro servicio, login-service. Añadimos dentro de la carpeta login-service un archivo llamado Dockerfile. Con unas cuantas líneas vamos a crear el fichero que servirá para crear la imagen:

        1 FROM python:3.8-slim-buster
        2 WORKDIR /app
        3 COPY ./app .
        4 RUN pip3 install -r requirements.txt
        5 CMD [ "uvicorn", "main:app", "--host=0.0.0.0"]

Línea 1: con el comando FROM, reutilizamos una plantilla que tiene docker para código Python, python:3.8-slim-buster
Línea 2: con el comando WORKDIR, establecemos el directorio de trabajo para la imagen
Línea 3: con el comando COPY, todo lo que hay en el directorio /app de nuestro proyecto se copiará en el directorio de trabajo de la imagen
Línea 4: con el comando RUN, instalamos todas las librería que están en el archivo requirements.txt de la imagen que se ha copiado en la linea anterior
Línea 5: con el comando CMD, se indica el comando y los parámetros que se deberán ejecutar cuando se implemente la imagen en un contenedor

Con este archivo ya podemos construir la imagen

Para construir la imagen del contenedor utilizamos el comando dentro del path donde se encuentra el Dockerfile

                $ docker build -t login-service --file Dockerfile .

Con este comando construimos la imagen del servicio. Tenemos el parámetro -t que hace referencia al tag con el que denominaremos a la imagen, el parámetro --file que hace referencia al nombre del archivo con la configuración de la imagen. Observa que al final hay un punto y es necesario para la ejecución.

y para realizar una implementación de la imagen en un contenedor:

                & docker run -p "4000:8000" login-service

En este comando implementamos la imagen en un contenedor. El parámetro -p hace referencia al puerto del host: puerto del contenedor. Mencionar que el puerto del contenedor tiene que ser 8000, ya que la aplicación que hemos creado se despliega en este puerto por defecto. Por último, hay que indicar el tag de la imagen que queremos que se implemente.

Si todo ha ido bien, una vez implementada la imagen en el contenedor, se ha debido de ejcutar el servidor uvicorn, y deberíamos poder acceder a la API utilizando el puerto 4000 como se muestra en los endpoints: http://127.0.0.1:4000; http://127.0.0.1:4000/test; http://127.0.0.1:4000/docs; http://127.0.0.1:4000/redoc


La gestión de contenedores e imágenes se puede hacer de una forma sencilla y gráfica utilizando la herramienta Docker Desktop.

## Base de datos con SQLAlchemy

Creamos una nueva carpeta dentro de ./app. Yo la lamaré db, y en ella guadaré todos los módulos para gestionar la base de datos. Lo primero, es añadir el fichero vacío __init__.py para convertir la carpeta /db en un sub paquete del proyecto, y después añadiré un fichero, database.py, que contedrá la implementación de la conexión a la base de datos. Para probar el código utilizaré una base de datos SQLite que se guardará en memoria. Más adelante se desplegará la base de datos como otro microservicio.

El fichero database.py

                from sqlalchemy import create_engine
                from sqlalchemy.ext.declarative import declarative_base
                from sqlalchemy.orm import sessionmaker

                SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

                engine = create_engine(SQLALCHEMY_DATABASE_URL, 
                                connect_args={"check_same_thread": False}
                                )

                SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

                Base = declarative_base()

Creamos una constante con la URL de la conexión a la base de datos. Después creamos un objeto engine, que la pasa como argumento de conexión la propiedad "check_same_thread" a False. Esto se realiza sólo en SQLite, ya que no es multihilo, es decir, usa un único hilo por petición. Debido a que FastAPI permite que haya difentes hilos con la misma petición por ser asícrona, hay que evitar que accidentalmente se pueda compartir la misma conexión para varias peticiones al atacar SQLite configurando la conexión.

SessionLocal es un objeto que permitirá manejar las sesiones de cada cliente. Para ello se llama al método sessionmaker que funciona como una factoría, que se encarga de crear una nueva sesión a la que adjuntará una de las conexiones disponibles en el pool del engine.

Creamos el objeto Base, llamando al método declarative_base(), que devolverá los metadatos de las tablas que se definan en la base de datos, que permite construir la estructura en el momento en que se inicialice la aplicación.

Habrá que definir el modelo de datos. Eso es lo que se hace en el archivo models.py, que define el modelo de SQLAlchemy que servirá para crear las tablas y sus relaciones

                from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
                from sqlalchemy.orm import relationship

                from .database import Base


                class User(Base):
                __tablename__ = "users"

                id = Column(Integer, primary_key=True, index=True)
                email = Column(String, unique=True, index=True)
                hashed_password = Column(String)
                is_active = Column(Boolean, default=True)
                role_id = Column(Integer, ForeignKey("roles.id"))
                
                role = relationship("Role")


                class Role(Base):
                __tablename__ = "roles"

                id = Column(Integer, primary_key=True, index=True)
                title = Column(String, unique=True)

Las clases heredan del objeto Base que creamos en el archivo database. Las clases representan las tablas y las relaciones que se dan entre ellas, en este caso, Many to One, varios usuarios pueden tener un role.

Ahora, necesitamos implementar esta funcionalidad cuando se inicialice la aplicación, se modificará el archivo main.py

        def init_db():
                roles=["Admin","User"]
                users = [
                        {"email":"admin@test.es",
                        "password":"1234",
                        "role_id":1}
                ]
                db = SessionLocal()
                for role in roles:
                        try:
                        admin= models.Role(title=role)
                        db.add(admin)
                        db.commit()
                        except Exception as e:
                        db.rollback()
                        print(e)
                        continue

                for user in users:
                        try:
                        u= models.User(email=user["email"],hashed_password = user["password"], role_id=user["role_id"])
                        db.add(u)
                        db.commit()
                        except Exception as e:
                        db.rollback()
                        print(e)
                        continue

                db.close()
                
        models.Base.metadata.create_all(bind=engine)

        app = FastAPI()
        app.include_router(testapi.router)

        init_db()

Nótese que se ha eliminado el enrutamiento que teniamos en este archivo, ya que lo dejaremos unicamente para inicializar la aplicación. Se ejecuta la función create_all() que generará el modelo definido de la base de datos, tablas y relaciones. También se crea una función init_db() que introduce algunos datos en la BD. Como el engine tiene configurado SQLite como base de datos se generará un archivo .db al inicializar el programa.

Otro tipo de modelos que se definen, son los modelos de Pydantic que heredan de la clase BaseModel perteneciente a la librería. Para no confundirlo con los modelos de la base de datos, vamos a crearlos en el archivo schemas.py

                from pydantic import BaseModel

                class Role(BaseModel):
                id: int
                title: str

                class Config:
                        orm_mode = True


                class User(BaseModel):
                id: int
                email: str
                is_active: bool
                role: Role

                class Config:
                        orm_mode = True

Esto permite serializar los objetos de las bases de datos para poder manejarlos en las peticiones y respuestas de la API de forma rápida y sencilla.