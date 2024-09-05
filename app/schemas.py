from typing import Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel): 
    email: EmailStr
    password: str 

class Login(User): 
    pass

class TokenData(BaseModel): 
    id: Optional[str] = None


class Blog(BaseModel):
    title: str 
    s_description: str 
    l_description: str 
     


