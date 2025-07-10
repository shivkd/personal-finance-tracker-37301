from pydantic import BaseModel, EmailStr

# PUBLIC_INTERFACE
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# PUBLIC_INTERFACE
class UserRead(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

# PUBLIC_INTERFACE
class Token(BaseModel):
    access_token: str
    token_type: str
