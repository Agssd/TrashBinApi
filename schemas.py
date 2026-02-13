from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    login: str
    password: str

class UserLogin(BaseModel):
    login: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str

class UserResponse(BaseModel):
    id: int
    username: str
    login: str
    points: int

class PointsUpdate(BaseModel):
    points: int

