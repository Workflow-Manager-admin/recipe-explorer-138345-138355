from fastapi import APIRouter, Depends
from ..schemas import UserRead
from ..models import User
from ..deps import get_current_user

router = APIRouter()

# PUBLIC_INTERFACE
@router.get("/me", response_model=UserRead, summary="Get current user info")
def get_me(current_user: User = Depends(get_current_user)):
    """Returns the current (authenticated) user's profile."""
    return current_user
