from fastapi import APIRouter, Depends

from app.database import get_db
from app.models import User
from app.schemas import UserOutput
from app.services.oauth2 import get_current_user

profile = APIRouter(prefix='/profile', tags=['Profile'])


@profile.get('/', status_code=200, response_model=UserOutput)
def get_my_profile(user: UserOutput = Depends(get_current_user), db=Depends(get_db)):
    profile = db.query(User).filter(User.id == user.id).first()
    return profile
