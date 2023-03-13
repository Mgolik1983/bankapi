from fastapi import APIRouter, HTTPException, status

from sqlalchemy.exc import IntegrityError
from Core.models import User
from Core.schemas import UserInfo, RegisterForm
router = APIRouter()

@router.post(
    '/register',
    response_model=UserInfo,
    response_model_exclude={'passwor', 'hashed_password','pk'},
    status_code=status.HTTP_201_CREATED
)

async def register_user(register_form: RegisterForm):
    user_info = UserInfo(**register_form.dict())
    user = User(**user_info.dict(exclude={'pk', 'password'}))
    try:
        await user.save()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='почта или имя пользователя не уникальны')
    else:
        return user_info
