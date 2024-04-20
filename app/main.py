from fastapi import FastAPI

from app.routers.users import router as user_router
from app.routers.auth import router as auth_router
from app.routers.post import router as post_router
from app.routers.post import app as post_app
from app.routers.profile import profile as profile_router
from app.routers.like import router as like_router
from app.routers.comment import router as comment_router

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(post_router)
app.include_router(post_app)
app.include_router(profile_router)
app.include_router(like_router)
app.include_router(comment_router)
