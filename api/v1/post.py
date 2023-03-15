from fastapi import APIRouter, HTTPException, Header, status
from jose import jwt, JWTError
from sqlalchemy.exc import IntegrityError

from Core.models import Post, User
from  Core.schemas import PostDetail, PostCreateForm
from Core.settings import EXPIRE_JWT_TOKEN, TOKEN_TYPE, ALGORITHM, SECRET_KEY

post_router = APIRouter(prefix='/post')


@post_router.post('/', response_model=PostDetail, status_code=status.HTTP_201_CREATED)
async def create_post(post_form: PostCreateForm, authorization: str = Header()):
    if authorization.startswith(TOKEN_TYPE):
        authorization = authorization.split()[1]
        try:
            payload = jwt.decode(authorization, SECRET_KEY, ALGORITHM)
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='token invalid')
        else:
            user = await  User.select(User.username == payload.get('sub'))
            if user:
                user = user[0]
                post = Post(**post_form.dict() | {'author_id': user.pk})
                try:
                    await post.save()
                except IntegrityError:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Post exists')
                else:
                    return PostDetail.from_orm(post)
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user has blocked')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid token type')