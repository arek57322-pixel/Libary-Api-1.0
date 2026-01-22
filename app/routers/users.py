from fastapi import APIRouter, Depends

from app.deps import get_current_user
from app import models

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def me(user: models.User = Depends(get_current_user)):
    return {"id": user.id, "email": user.email, "role": user.role}
