from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.database import get_db
from app.models import Like, Post
from app.schemas import LikeInput, UserOutput
from app.services.oauth2 import get_current_user

router = APIRouter(prefix='/like', tags=['Like'])


@router.post('/', status_code=200)
def like_to_post(post: LikeInput = Depends(), db: Session = Depends(get_db),
                 user: UserOutput = Depends(get_current_user)):
    post_e = db.query(Post).filter(Post.id == post.post_id).first()

    if post_e is None:
        raise HTTPException(detail='Post doesnt exists', status_code=status.HTTP_204_NO_CONTENT)

    query = db.query(Like).filter(Like.post_id == post.post_id, Like.owner_id == user.id)

    if query.first() is None:
        like = Like(**post.dict(), owner_id=user.id)
        db.add(like)
        db.commit()
        db.refresh(like)
        return {'message': 'Post has been liked'}
    else:
        query.delete()
        db.commit()
        return {'message': 'Post has been unliked'}
