from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, JOSEError
from  db.schemas import LoginUser, User, UserInDB
from auth.authservice import AuthService
from auth.tokenutils import TokenUtils
from db.dependencies import get_db
from sqlalchemy.orm import Session
from config import Settings

#pip install python-multipart -> es necesario para enviar el username y el password
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer (tokenUrl="login")

router = APIRouter(prefix="",
    tags=["authentication"])

auth_service = AuthService()
settings = Settings()
token_utils = TokenUtils (secret_key=settings.SECRET_KEY,
                            algorithm = settings.ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):

    credential_exception = HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Credenciales incorrectas",
                            headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        print(settings.SECRET_KEY)
        try:
            payload = token_utils.decode_token(token)
            id:int = payload.get('sub')
        except JOSEError as e:
            print(e)
        user = auth_service.get_user_by_id(db,id)

        if user is None:
            raise credential_exception

    except JWTError:
        raise credential_exception

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Credenciales de usuario desactivadas")
    return current_user



@router.get("/")
async def root():
    return {"message": "Hello World from auth"}

@router.post("/login")
async def login(form_data : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_service.login_user(db,form_data.username,form_data.password)

    if user == None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_access = token_utils.create_token(data= user.get_payload())

    return {"access_token": token_access, "token_type": "Bearer"}         

@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
