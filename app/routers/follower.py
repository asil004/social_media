from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Followers, User
from app.schemas import FollowerOutput, UserOutput, RequestOutput, AccRejReq, DoFollow, AllFriendsSchemaFollower, \
    AllFriendsSchemaFollowing
from app.services.oauth2 import get_current_user

router = APIRouter(prefix='/follower', tags=['follower'])


# @router.get('/my', status_code=200, response_model=list[FollowerOutput])
# def get_my_followers(db: Session = Depends(get_db), user: UserOutput = Depends(get_current_user)):
#     query = db.query(Followers).filter(Followers.user_id == user.id).all()
#
#     return query


@router.post('/{user_id}', status_code=201)
def add_follower(user_id: int, db: Session = Depends(get_db),
                 user: UserOutput = Depends(get_current_user)):
    user_ = db.query(User).filter(User.id == user_id).first()

    if not user_:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')

    if user_id == user.id:
        raise HTTPException(status_code=403, detail='You cant follow yourself')

    follower = Followers(following_id=user.id, followers_id=user_.id)
    db.add(follower)
    db.commit()
    db.refresh(follower)
    return {'message': 'Follower added !'}


@router.post('/is-following/{user_id}', status_code=201)
def is_follower(user_id: int, db: Session = Depends(get_db),
                user: UserOutput = Depends(get_current_user)):
    user_ = db.query(User).filter(User.id == user_id).first()

    if not user_:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')

    follower = db.query(Followers).filter(Followers.following_id == user_.id, Followers.followers_id == user.id)

    if not follower.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You cant follow user')

    follower.update({'is_following': True})
    db.commit()
    return {'message': 'User followed'}


@router.delete('/{user_id}', status_code=status.HTTP_200_OK)
def delete_follower(user_id: int, db: Depends = Depends(get_db), user: UserOutput = Depends(get_current_user)):
    user_ = db.query(User).filter(User.id == user_id).first()

    if not user_:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')

    follower = db.query(Followers).filter(Followers.following_id == user_.id, Followers.followers_id == user.id)
    if not follower.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You cant follow user')

    follower.delete()
    db.commit()
    return {'Message': 'User deleted'}


@router.get('/all-friends', status_code=200,
            response_model=tuple[list[AllFriendsSchemaFollower], list[AllFriendsSchemaFollowing]])
def my_followers(db: Session = Depends(get_db), user: UserOutput = Depends(get_current_user)):
    follower = db.query(Followers).filter(Followers.following_id == user.id,
                                          Followers.is_following == True).all()
    following = db.query(Followers).filter(Followers.followers_id == user.id,
                                           Followers.is_following == True).all()
    return follower, following

# @router.get('/my-requests', status_code=200, response_model=list[FollowerOutput])
# def my_requests(db: Session = Depends(get_db), user: UserOutput = Depends(get_current_user)):
#     query = db.query(Followers).filter((Followers.following_id == user.id | Followers.followers_id == user.id),
#                                        Followers.is_following == False).all()
#     return query

# # My requests
# @router.get('/requests', status_code=200, response_model=list[RequestOutput])
# def get_requests(db: Session = Depends(get_db), user: UserOutput = Depends(get_current_user)):
#     query = db.query(Requests).filter(Requests.user_id == user.id).all()
#
#     return query
#
#
# @router.put('/accept-or-reject', status_code=status.HTTP_201_CREATED)
# def accept_or_reject_requests(request_rej_acc: AccRejReq = Depends(), db: Session = Depends(get_db),
#                               user: UserOutput = Depends(get_current_user)):
#     query = db.query(Requests).filter(Requests.id == request_rej_acc.request_id).first()
#
#     if query is None:
#         raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='Request doesnt exists')
#     else:
#         if request_rej_acc.is_accept:
#             follower = Followers(user_id=user.id)
#             db.add(follower)
#             db.commit()
#             db.refresh(follower)
#
#             db.delete(query)
#             db.commit()
#             return {'message': 'Followers successfully added!'}
#         else:
#             db.delete(query)
#             db.commit()
#             return {'message': 'Request rejected'}
