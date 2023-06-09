from datetime import datetime

from fastapi import APIRouter, HTTPException, Header, status, Query, Depends, BackgroundTasks
from jose import jwt, JWTError
from sqlalchemy.exc import IntegrityError

from core.models import Post, User
from core.schemas import PostDetail, PostCreateForm
from core.settings import EXPIRE_JWT_TOKEN, TOKEN_TYPE, ALGORITHM, SECRET_KEY
from core.utils.qrcode import generate_qrcode
post_router = APIRouter(prefix='/post')


async def validate_token(authorization: str = Header()) -> User:
    if authorization.startswith(TOKEN_TYPE):
        authorization = authorization.split()[1]
        try:
            payload = jwt.decode(authorization, SECRET_KEY, ALGORITHM)
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='token invalid')
        else:
            user = await User.select(User.username == payload.get('sub'))
            if user:
                return user[0]
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user has blocked')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid token type')


@post_router.post('/', response_model=PostDetail, status_code=status.HTTP_201_CREATED)
async def create_post(post_form: PostCreateForm, user: User = Depends(validate_token)):
    post = Post(**post_form.dict() | {'author_id': user.pk})
    try:
        await post.save()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='post exist')
    else:
        return PostDetail.from_orm(post)


@post_router.get('/', response_model=list[PostDetail])
async def posts():
    objs = await Post.select(order_by=Post.date_created.desc())
    return [PostDetail.from_orm(obj) for obj in objs]


@post_router.get('/{post_id}', response_model=PostDetail)
async def post_detail(
        background_tasks: BackgroundTasks,
        post_id: int = Query(
            ge=1,
            title='Post Unique ID'
        )
):
    post = await Post.get(post_id)
    if post:
        background_tasks.add_task(generate_qrcode, post.title)
     #   with open('img.jpg', 'rb') as file:
     #       background_tasks.add_task(send_mail, 'mgolik1983@g,ail.com', post.title, post.body, file=file.read())
        return PostDetail.from_orm(post)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')


@post_router.delete('/{post_id}', status_code=status.HTTP_202_ACCEPTED)
async def delete_post(
        post_id: int = Query(
            ge=1,
            title='Post Unique ID'
        ),
        user: User = Depends(validate_token)
):
    post = await Post.get(post_id)
    if post:
        if post.author_id == user.pk:
            await post.delete()
            return {'detail': 'post deleted successfully'}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='you are not author of the post'
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')


@post_router.put('/', status_code=status.HTTP_202_ACCEPTED)
async def update_post(
        post_detail: PostDetail,
        user: User = Depends(validate_token)
):
    post = await Post.get(post_detail.pk)
    if post:
        if post.author_id == user.pk:
            post.title = post_detail.title
            post.body = post_detail.body
            post.date_created = datetime.now()
            try:
                await post.save()
            except IntegrityError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='post exist')
            return PostDetail.from_orm(post)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='you are not author of the post'
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
