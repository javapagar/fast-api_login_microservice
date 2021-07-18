from fastapi import FastAPI
from test import testapi

app = FastAPI()
app.include_router(testapi.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}