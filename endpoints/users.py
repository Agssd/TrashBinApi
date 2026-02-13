from fastapi import APIRouter, Header, HTTPException, Depends, status
from typing import Annotated
from ..security import decode_token
from ..services.user_service import get_user_by_login, update_user_points
from ..schemas import UserResponse, PointsUpdate

router = APIRouter()

def get_current_user(
    authorization: Annotated[str | None, Header(alias="Authorization")] = None
) -> str:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
        )
    parts = authorization.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer" or not parts[1]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization format",
        )
    token = parts[1]
    return decode_token(token)

@router.get("/me", response_model=UserResponse)
def get_profile(current_user: str = Depends(get_current_user)):
    return get_user_by_login(current_user)

@router.patch("/me/points", response_model=UserResponse)
def update_points(data: PointsUpdate, current_user: str = Depends(get_current_user)):
    update_user_points(current_user, data.points)
    return get_user_by_login(current_user)