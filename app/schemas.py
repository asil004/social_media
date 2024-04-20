from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOutput(BaseModel):
    id: int
    email: EmailStr
    created: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int


class CommentToPost(BaseModel):
    id: int
    content: str
    created: datetime


class LikeOutput(BaseModel):
    id: int
    owner: UserOutput


# post
class PostOutput(BaseModel):
    id: int
    title: str
    content: str
    comments: list[CommentToPost]
    likes: list[LikeOutput]
    created: datetime

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    title: str
    content: str


class LikeInput(BaseModel):
    post_id: int


class CommentDel(BaseModel):
    id: int


class CommentInput(BaseModel):
    post_id: int
    content: str


class CommentOutput(CommentToPost):
    post: PostOutput
    owner: UserOutput


class FollowerOutput(BaseModel):
    id: int
    user: UserOutput


class RequestOutput(BaseModel):
    id: int
    user: UserOutput


class DoFollow(BaseModel):
    user_id: int


class AccRejReq(BaseModel):
    request_id: int
    is_accept: bool
