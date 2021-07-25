# fast-api_login_microservice

https://realpython.com/fastapi-python-web-apis/

## Stack
SO Mac OS 10.13.6
Python 3.9.6
Docker 20.10.7
Dbeaver lite 21.1.0


## Preparando el entorno
Lo primero, será crear un entorno virtual dentro de la carpeta de la aplicación, para poder instalar las librerías necesarias.

        $ python3 -m venv venv

Se activa el entorno

        $ source venv/bin/activate

Instalo la librería fast-api y el servidor uvicorn, que será el encargado de manejar las peticiones a la API. Con este servidor la aplicación será completamente robusta en producción, lo que simplifica bastante la tarea.

        $ pip install fastapi uvicorn[standard]

También, se instala la librería SQLAlchemy, que es un ORM con el que gestionaremos la base de datos que complementará la aplicación.

        $ pip install SQLAlchemy

Podemos ver todas las librerías instaladas con el comando

        $ pip freeze

y si queremos guardar las dependencias en el fichero requirements.txt

        $ pip freeze > requirements.txt

Ejecutaré el comando anterior siempre que hago un pip install en el entorno.


## Estructura del proyecto
En la raíz de la carpeta de la aplicación crearemos un archivo __init__.py vacío. Este archivo marcará la carpeta como un paquete python. En cada carpeta nueva que creemos dentro, también situaremos un archivo __init__.py, convirtiéndolo en un sub-paquete. DE igual manera, los archivos .py que se encuentren dentro de estas carpetas serán módulos o sub-módulos de python. De esta manera se podrá importar código de cualquier archivo a otro.

Para empezar crearemos la siguiente estructura

        .
        ├── fast-api-login-microservice 
                ├──login-service
                        ├── app                  # es el paquete Python
                        │   ├── __init__.py      # este fichero convierte a la carpeta "app" en un paquete Python
                        │   ├── main.py          # Módulo "main"
                        │   └── auth             # "auth" es un sub-paquete Python del paquete "app"
                        │   │   ├── __init__.py  # convierte a la carpeta "auth" en un sub-paquete Python
                        │   │   ├── authapi.py   # Sub-módulo"authapi"


Como se comentó antes, los archivos init se dejarán vacíos. El módulo main será el encargado de crear la aplicación, y una primera prueba:

                from fastapi import FastAPI

                app = FastAPI()

                @app.get("/")
                async def root():
                return {"message": "Hello World"}

con estas líneas ya podríamos ejecutar el servicor uvicorn

                $ uvicorn main:app

y cuando esté levantado, podemos acceder a http://127.0.0.1:8000

Siguiendo con la prueba vamos a completar el módulo authapi. La anterior estructura sería la base de un proyecto grande, en el que cada subcarpeta nos ayudaría a tener más ordenado el código. EL archivo authapi contendrá el enrutamiento a otro recursos de la api que se deberá registrar en la aplicación principal. En Flask, esto se hacía a través de los Blueprints, en FastAPI se utilizará APIRouter. Vamos a ver un ejemplo con authapi:

                from fastapi import APIRouter

                router = APIRouter(prefix="/auth",
                                tags=["authentication"])

                @router.get("/")
                async def root():
                return {"message": "Hello World from auth"}

Con la clase APIRouter creamos un nuevo endpoint, con la propiedad prefix daremos la base de la url y con la propiedad tags definimos etiquetas que definirán las entradas en la documentación de la API.

Ahora, habrá que retocar el módulo main para registrar este nuevo enrutamiento:

                from fastapi import FastAPI
                from auth import authapi

                app = FastAPI()
                app.include_router(authapi.router)

                @app.get("/")
                async def root():
                return {"message": "Hello World"}

Con estos sencillos pasos tendríamos disponible el endpoint http://127.0.0.1:8000/auth

## Documentación de la API
Otra de las ventajas de usar FastAPI es que permite la construcción automática de la documentación de la API, aunque se puede hacer de diferentes maneras, dos están incluidas por defecto:

* Swagger UI http://127.0.0.1:8000/docs
* ReDoc http://127.0.0.1:8000/redoc


## Base de datos con SQLAlchemy
Creamos una nueva carpeta dentro de ./app. Se llamará db, y en ella estarán todos los módulos para gestionar la base de datos. Lo primero, es añadir el fichero vacío __init__.py para convertir la carpeta /db en un sub paquete del proyecto, y después añadiré un fichero, database.py, que contiene la implementación de la conexión a la base de datos. Para probar el código utilizaré una base de datos SQLite que se guardará en memoria. Más adelante se desplegará la base de datos como otro microservicio.

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

Creamos una constante con la URL de la conexión a la base de datos. Después creamos un objeto engine, que la pasa como argumento de conexión la propiedad "check_same_thread" a False. Esto se realiza sólo en SQLite, ya que no es multihilo, es decir, usa un único hilo por petición. Debido a que FastAPI permite que haya diferentes hilos con la misma petición por ser asíncrona, hay que evitar que accidentalmente se pueda compartir la misma conexión para varias peticiones al atacar SQLite configurando la conexión.

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

Ahora, necesitamos implementar esta funcionalidad cuando se inicialice la aplicación, se crea el módulo fill_db.py

                from db import models
                from db.database import SessionLocal

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

que insertará un usuario administrador. Será necesario llamarlo desde el archivo main.py, necesita importar el método init_db y llamarlo:

                from fastapi import FastAPI
                from auth import authapi

                from db import models
                from db.database import SessionLocal, engine
                from db.fill_db import init_db
                
                models.Base.metadata.create_all(bind=engine)

                app = FastAPI()
                app.include_router(authapi.router)

                init_db()

Nótese que se ha eliminado el enrutamiento que teníamos en este archivo, ya que se deja únicamente para inicializar la aplicación. Se ejecuta la función create_all() que generará el modelo definido de la base de datos, tablas y relaciones. También se llama a la función init_db(). Como el engine tiene configurado SQLite como base de datos se generará un archivo .db al inicializar el programa.

## Variables de configuración

Una buena práctica es tener la configuración de forma independiente, y no "hardcodeada" en nuestra función. Para refactorizar esto, se va a utilizar un fichero de configuración, .env,que se cargará utilizando Pydantic. El fichero no está subido al proyecto de github, ya que el .gitignore lo impide, en estos ficheros se suelen guardar información sensible como los datos de conexión. En la raiz del proyecto, crearemos el archivo config.py para conectar a SQLite

                from pydantic import BaseSettings

                class Settings(BaseSettings):
                        db_url : str = "url_con"

                        class Config:#desde fichero .env
                                env_file=".env"

La clase Settings hereda de BaseSettings y será la encargada de guardar las propiedades definidas en el archivo .env. Además, tendrá la clase Config, que será la encargada de leer el archivo de configuración y guardarla en la propiedad correspondiente.

Un ejemplo de archivo .env con la configuración para SQLite bastaría con la siguiente línea:

                db_url = "sqlite:///./sql_app.db"

En este caso está configurada la base de datos SQLite, pero podría ser cualquier otra. Habrá que utilizar esta variables en vez de pasarla directamente como se estaba haciendo en el archivo db/database.py, se modifica añadiendo:

                from config import Settings

                settings = Settings()

                SQLALCHEMY_DATABASE_URL = settings.db_url

en vez de

                SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"


## Authenticación

### Login
Necesitamos es instalar la librería python-multipart

                $pip install python-multipart

Para dar seguridad a las claves que se guardarán en la base de datos necesitamos protegerlas con un algoritmo de hashing. Esto permite codificar la contraseña del usuario para guardar este código resultante en la base de datos. Para el login, el usuario introducirá su contraseña en texto plano y nuestra aplicación será la encargada de codificarla con el mismo algoritmo de hashing utilizado para comprobar que coinciden, lo que le permitirá obtener los permisos necesarios. En caso de robo de la base de datos, las contraseñas no se podrán decodificar de una forma sencilla.
Para este proceso necesitamos otra librería, passlib, que soporta distintos algoritmos de hashing. La recomendación es utilizar bcrypt

                $ pip install passlib[bcrypt]

La implementación del hasing se hará en el módulo /db/models.py que es donde tenemos la clase User que usará este método para crear el objeto. Para hacer el hashing necesitamos un "context" en le módulo models importaremos:

                from passlib.context import CryptContext

### JWT
y python-jose, para generar y verificar JWT. Esta librería necesita un backend extra para realizar las tareas de criptografía, en el siguiente comando se usará pyca/cryptography

                $ pip install python-jose[cryptography]

Para crear la clave secreta que permitirá firmar el JWT esiste un comando

                $ openssl rand -hex 32

La cadena que nos devuelve es la clave secreta. Un buen sítio para guardar este parámetro es el fichero de configuración del entorno .env. También le diremos el algoritmo de coidficación que se utilizará para el JWT, que normalmente será el HS256, y que también guardamos en una constante. Añadiremos las siguientes lineas al final del fichero .env

                SECRET_KEY = "THE_BEST_SECRET_KEY"
                ALGORITHM = "HS256"

Una vez hecho esto, modifcaremos config.py, añadiendo las propiedades de la clase Setting para poder leerlas:

                SECRET_KEY : str
                ALGORITHM : str

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

Si todo ha ido bien, una vez implementada la imagen en el contenedor, se ha debido de ejcutar el servidor uvicorn, y deberíamos poder acceder a la API utilizando el puerto 4000 como se muestra en los endpoints: http://127.0.0.1:4000; http://127.0.0.1:4000/auth; http://127.0.0.1:4000/docs; http://127.0.0.1:4000/redoc


La gestión de contenedores e imágenes se puede hacer de una forma sencilla y gráfica utilizando la herramienta Docker Desktop.


## Docker-compose: microservicios en producción
Antes se hablo de microservicios, pero hasta ahora tenemos una única aplicación con un SQLite integrado. Vamos a ir un poco más allá, aprovechando el poder de docker para crear otro microservicio que contenga un servidor de base de datos como postgreSQL integrado con el microservicio de login. Para esto, se utiliza Docker-compose, una herramienta que se instala junto con docker. Lo que nos permite esta herramienta es unificar un montón de microservicios relacionados y poder levantarlos con muy poco esfuerzo. Esto se consigue creando un fichero de configuración donde iremos añadiendo nuestros microservicios con la referencia a los Dockerfile conrrespondiente a cada microservicio y su configuración cuando esto corresponda. Docker-compose se suele utilizar más para desarrollo, dejando a Kubernetes que haga lo propio en producción.

Este fichero es el docker-compose.yml, y de momento se va a añadir el único microservicio que tenemos. Este archivo tiene que estar al mismo nivel que las carpetas de los diferentes microservicios.

#version docker-compose
version: '3.8'
#se empiezan a describir los servicios que se levantarán
services:
    #nombre que le damos al servicio
    login-service:
        #tag de la imagen del servicio
        image: login-service
        # para crear la imagen
        build:
            #se referencia donde está el dockerfile
            context: ./login-service
            #nombre del dockerfile
            dockerfile: Dockerfile
        # nombre que se le dará al contenedor que se cree a partir de la imagen
        container_name: login-service
        #referencia al fichero de configuración del entorno
        env_file: 
            - ./login-service/app/.env
        #enlace de puertos host y container
        ports:
            #puerto del host:puerto del container (en el dockerfile no especificamos puerto al arrancar uvicorn, por lo que por defecto es 8000)
            - "4000:8000"
        #impedirá que se reinicie en caso de fallo, como estamos en desarrollo nos interesa saber cuando falla
        restart: "no"

Con el siguiente comando se creará la imagen del microservicio y se levantará una instancia

                $ docker-compose up --build

Si todo ha ido bien, se puede probar con cualquier navegador localhost:4000/auth. Se recomienda, para parar los servicios utilizar el comnando:
                
                $ docker-compose down

Puede que la facilidad que nos aporta docker-compose no parezca mucha para un único servicio. En realidad hemos reducido los dos comandos utilizados con docker, build y run, a uno. Pero si añadimos 10 servicios más, con docker, desplegandolos uno a uno, sería una tarea tediosa que nos podemos ahorrar con docker-compose. Vamos a añadir una base de datos como un servicio diferente, es tan facil como añadir las siguientes lineas al archivo docker-compose.yml dentro de services:
        
#version: '3.8'

services:
#nombre de la imagen de la bd
    login-db:
        #nombre de la imagen que descargará docker   
        image: postgres:13-alpine
        #nombre del contenedor
        container_name: login-db
        #los datos de conexión de la bd
        env_file: 
            - ./login-service/app/.env
        #port-host:port-container
        ports:
            - "4000:5432"
        #La base de datos tiene que reiniciarse si hay algún problema
        restart: always

    login-service:
        image: login-service
        build:
            context: ./login-service
            dockerfile: Dockerfile
        container_name: login-service
        env_file: 
            - ./login-service/app/.env
        ports:
            - "4001:8000"
        #relacionamos el microservicio api con la bd
        depends_on:
            - login-db
        restart: "no"

Nótese que los puertos del host se ha reasignado dando el puerto 4000 a la base de datos y el 4001 a la API. La base de datos podría ser el mismo puerto, 5432, pero en mi caso ya tengo ese puerto ocupado.

Antes de ejecutar, hay que cambiar partes del código para configurar postgreSQL. Primero añadiremos las variables oprotunas al fichero /login-service/app/.env

                POSTGRES_USER=postgres
                POSTGRES_PASSWORD=postgres
                POSTGRES_SERVER=db
                POSTGRES_PORT=5432
                POSTGRES_DB=postgres

Ahora, hay que actualziar la conexión a la base de datos en el archivo /login-service/app/db/database.py, concretamente la asignación de la variable SQLALCHEMY_DATABASE_URL

        SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

También, en el mismo archivo, se modificará la variable engine, concretamente se eliminará el parámetro connect_args del método create_engine:

        engine = create_engine(SQLALCHEMY_DATABASE_URL, 
                #connect_args={"check_same_thread": False}
                )

Ejecutamos de nuevo el comando:

        $ docker-compose up --build

Puedes acceder a la base de datos con tu cliente favorito, yo uso DBeaver. Recuerda que en este ejemplo se ha sustituido el puerto 5432 por defecto de postgreSQL por el 4000 a la hora de conectar. Podrás ver como se han insertado el registro de inicio.

## Serialización
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