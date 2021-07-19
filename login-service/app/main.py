from fastapi import FastAPI
from test import testapi

from db import models
from db.database import SessionLocal, engine
from db.fill_db import init_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(testapi.router)

init_db()