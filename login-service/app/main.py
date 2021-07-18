from fastapi import FastAPI
from test import testapi

from db import models
from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(testapi.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}