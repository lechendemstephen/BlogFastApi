from jose import jwt, JWTError # type: ignore
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from . import schemas
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET KEY 
# ALGORITHM
# ACCESS_TOKEN_EXPIRE_MINUTES 
SECRET_KEY = settings.secret_key
ALGORITHM =  settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# creating access token 
def create_access_token(data: dict): 
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# verify the access token 
def verify_access_token(token: str, credential_exception): 
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized access')
    id: str = payload.get('user_id')
    if not id: 
        raise credential_exception
    token_data = schemas.TokenData(id=str(id))

    return token_data

# getting the current user 

def current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized access', headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credential_exception)


