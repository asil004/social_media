from fastapi import APIRouter, Depends, HTTPException, status

from app.models import Post, User
from app.database import get_db
from app.schemas import PostCreate, PostOutput, UserOutput
from app.services.oauth2 import get_current_user

router = APIRouter(prefix='/my-post', tags=['MyPost'])
app = APIRouter(prefix='/posts', tags=['Posts'])


# router
@router.post('/create', status_code=201, response_model=PostOutput)
def post_create(post: PostCreate, db: Depends = Depends(get_db), user: UserOutput = Depends(get_current_user)):
    post = Post(**post.dict(), owner_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get('/get', status_code=200, response_model=list[PostOutput])
def post_get_my(db: Depends = Depends(get_db), user: UserOutput = Depends(get_current_user)):
    return db.query(Post).filter(User.id == user.id).all()


@router.put('/update/{post_id}', status_code=200, response_model=PostOutput)
def update_my_post(post_id: int, post_data: PostCreate, db: Depends = Depends(get_db),
                   user: UserOutput = Depends(get_current_user)):
    query = db.query(Post).filter(Post.id == post_id)
    post = query.first()

    if not post:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='Post doesnt exists!')
    #
    # if int(post.owner_id) != int(user.id):
    #     return HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
    #                          detail='You dont have permission to update this post!')

    query.update(post_data.dict(), synchronize_session=False)

    db.commit()
    return post


@router.delete('/delete/{post_id}', status_code=200, response_model=list[PostOutput])
def delete_my_post(post_id: int, db: Depends = Depends(get_db),
                   user: UserOutput = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id, Post.owner_id == user.id).first()

    if not post:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='Post doesnt exists!')

    post.delete()

    db.commit()
    return post


# ----------------------------------------------------------> app
@app.get('/all', status_code=200, response_model=list[PostOutput])
def post_get_all(db: Depends = Depends(get_db)):
    post = db.query(Post).all()
    return post
