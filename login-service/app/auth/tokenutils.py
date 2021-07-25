from datetime import datetime, timedelta
from typing import Optional
from jose import jwt

class TokenUtils():

    def __init__(self,secret_key : str, algorithm : str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_token(self,data: dict, expires_delta: Optional [timedelta] = None):
        data_to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        
        data_to_encode.update({'exp':expire})
        return jwt.encode(data_to_encode, self.secret_key, algorithm = self.algorithm)

    def decode_token(self,token: str):
        return jwt.decode(token,secret_key,algorithms = [self.algorithm])