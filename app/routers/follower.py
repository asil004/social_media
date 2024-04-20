from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Followers, Requests, User
from app.schemas import FollowerOutput, UserOutput, RequestOutput, AccRejReq, DoFollow
from app.services.oauth2 import get_current_user

router = APIRouter(prefix='/follower', tags=['follower'])


@router.get('/my', status_code=200, response_model=list[FollowerOutput])
def get_my_followers(db: Session = Depends(get_db), user: UserOutput = Depends(get_current_user)):
    query = db.query(Followers).filter(Followers.user_id == user.id).all()

    return query


@router.put('/do-follow', status_code=200)
def do_followers(do_follow: DoFollow = Depends(), db: Session = Depends(get_db),
                 user: UserOutput = Depends(get_current_user)):
    query = db.query(User).filter(User.id == do_follow.user_id).first()

    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user doesnt exists')

    do_follow = Requests(user_id=user.id)
    db.add(do_follow)
    db.commit()
    db.refresh(do_follow)
    return {'message': 'Request for following successfully sended !'}


@router.delete('/delete-my-follower/{user_id}', status_code=status.HTTP_200_OK)
def delete_my_follower(user_id: int, db: Depends = Depends(get_db)):
    follower = db.query(Followers).filter(Followers.user_id == user_id).first()

    if not follower:
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='Follower doesnt exists!')

    follower.delete()
    db.commit()
    return follower


# My requests
@router.get('/requests', status_code=200, response_model=list[RequestOutput])
def get_requests(db: Session = Depends(get_db), user: UserOutput = Depends(get_current_user)):
    query = db.query(Requests).filter(Requests.user_id == user.id).all()

    return query


@router.put('/accept-or-reject', status_code=status.HTTP_201_CREATED)
def accept_or_reject_requests(request_rej_acc: AccRejReq = Depends(), db: Session = Depends(get_db),
                              user: UserOutput = Depends(get_current_user)):
    query = db.query(Requests).filter(Requests.id == request_rej_acc.request_id).first()

    if query is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='Request doesnt exists')
    else:
        if request_rej_acc.is_accept:
            follower = Followers(user_id=user.id)
            db.add(follower)
            db.commit()
            db.refresh(follower)

            db.delete(query)
            db.commit()
            return {'message': 'Followers successfully added!'}
        else:
            db.delete(query)
            db.commit()
            return {'message': 'Request rejected'}
