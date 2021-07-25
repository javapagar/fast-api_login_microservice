from fastapi import APIRouter, Depends, HTTPException, status
from  db.schemas import LoginUser, User, UserInDB
from auth.authservice import AuthService
from auth.tokenutils import TokenUtils
from db.dependencies import get_db
from sqlalchemy.orm import Session
from config import Settings

#pip install python-multipart -> es necesario para enviar el username y el password
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

oauth2_scheme = OAuth2PasswordBearer (tokenUrl="auth/login")

router = APIRouter(prefix="/auth",
    tags=["authentication"])

auth_service = AuthService()
settings = Settings()
token_utils = TokenUtils (secret_key=settings.SECRET_KEY,
                            algorithm = settings.ALGORITHM)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



@router.get("/")
async def root():
    return {"message": "Hello World from auth"}

@router.post("/login")
async def login(form_data : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_service.login_user(db,form_data.username,form_data.password)

    if user == None:
        raise HTTPException(status_code=401, detail="Usuario o password incorrecto")
    
    token_access = token_utils.create_token(data= user.get_payload())

    return {"access_token": token_access, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/users", response_model=User)
async def get_user(login_user:LoginUser, db: Session = Depends(get_db)):
    return auth_service.get_user_by_username(db,login_user.email)