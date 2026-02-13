from fastapi import APIRouter
from ..schemas import UserCreate, UserLogin, TokenResponse, RefreshRequest
from ..services.auth_service import register_user, login_user
from ..security import decode_token, create_access_token 

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
def register(user: UserCreate):
    register_user(user.username, user.login, user.password)
    token_data = login_user(user.login, user.password)
    return TokenResponse(
        access_token=str(token_data[0]), 
        refresh_token=str(token_data[1])
    )

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin):
    token_data = login_user(user.login, user.password)
    return TokenResponse(
        access_token=str(token_data[0]), 
        refresh_token=str(token_data[1])
    )

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(body: RefreshRequest):
    login = decode_token(body.refresh_token)
    new_access = create_access_token(login)
    return TokenResponse(access_token=new_access, refresh_token=body.refresh_token)
