from fastapi import APIRouter

router = APIRouter(prefix="/auth",
    tags=["authentication"])

@router.get("/")
async def root():
    return {"message": "Hello World from auth"}