from fastapi import FastAPI
from test import testapi

from db import models
from db.database import SessionLocal, engine

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