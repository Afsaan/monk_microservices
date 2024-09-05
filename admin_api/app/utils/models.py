from pydantic import BaseModel

class Login(BaseModel):
    email: str
    password: str

class User(Login):
    name: str

class AddUser(User):
    securityCode: str

class ResetPassword(BaseModel):
    email: str
    newPassword: str
    securityCode: str