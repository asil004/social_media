from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.database import get_db
from app.models import Like, Post, Comment
from app.schemas import LikeInput, UserOutput, CommentInput, CommentOutput, CommentDel
from app.services.oauth2 import get_current_user

router = APIRouter(prefix='/comment', tags=['Comment'])


@router.post('/', status_code=200, response_model=CommentOutput)
def comment_to_post(post: CommentInput = Depends(), db: Session = Depends(get_db),
                    user: UserOutput = Depends(get_current_user)):
    post_e = db.query(Post).filter(Post.id == post.post_id).first()

    if post_e is None:
        raise HTTPException(detail='Post doesnt exists', status_code=status.HTTP_204_NO_CONTENT)

    comment = Comment(**post.dict(), owner_id=user.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.delete('/', status_code=200)
def delete_post(comm: CommentDel = Depends(), db: Session = Depends(get_db)):
    post_e = db.query(Comment).filter(Comment.id == comm.id)

    if post_e.first() is None:
        raise HTTPException(detail='Comment doesn\'t exists', status_code=status.HTTP_204_NO_CONTENT)

    db.delete(post_e)
    db.commit()
    return {'message': 'Comment deleted!'}
