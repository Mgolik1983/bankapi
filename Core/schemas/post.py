from pydantic import BaseModel, Field
from datetime import datetime


class PostCreateForm(BaseModel):
    title: str = Field(
        max_length=128,
        title='Post title',
        description='Post Uniue Title'
    )
    body: str = Field(
        title='Post body',
        description='Post body'
    )
class PostDetail(PostCreateForm):
    pk: int = Field(
        ge=1,
        title='Post id',
        description='Post Uniue Id'
    )
    date_created: datetime = Field(
        title='Post Date Created',
        description='Post Date Created',
    )
    author_id: int = Field(
        ge=1,
        title='Post Author ID',
        description='Post Author Unique ID'
    )
    class Config:
        orm_mode = True
