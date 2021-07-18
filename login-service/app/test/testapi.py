from fastapi import APIRouter

router = APIRouter(prefix="/test",
    tags=["tester"])

@router.get("/")
async def root():
    return {"message": "Hello World from test"}