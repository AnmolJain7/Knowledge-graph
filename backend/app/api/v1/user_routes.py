from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse
)

from app.services.user_service import (service)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("",response_model=UserResponse)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):

    try:
        return service.create_user(db, payload)

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = service.get_user(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.get("")
def get_all_users(db: Session = Depends(get_db)):
    return service.get_all_users(db)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):

    try:
        updated = service.update_user(db, user_id, payload)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return updated


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    deleted = service.delete_user(db, user_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message":
        "User deleted successfully"
    }
