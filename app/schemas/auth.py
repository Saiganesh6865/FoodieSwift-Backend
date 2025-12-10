from pydantic import BaseModel, EmailStr

class RegisterIn(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "merchant"

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    role: str
