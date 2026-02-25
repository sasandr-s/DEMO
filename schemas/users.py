from pydantic import BaseModel, EmailStr

class UserReg(BaseModel):
    login: str
    email:EmailStr
    password: str
    phone: str
    full_name: str

class UserLogin(BaseModel):
    login: str
    password: str