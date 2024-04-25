from fastapi import FastAPI
from starlette_admin.auth import BaseAuthProvider

from app.database import engine
from app.models import User, Post, Comment, Like, Followers
from app.routers.users import router as user_router
from app.routers.auth import router as auth_router
from app.routers.post import router as post_router
from app.routers.post import app as post_app
from app.routers.profile import profile as profile_router
from app.routers.like import router as like_router
from app.routers.comment import router as comment_router
from app.routers.follower import router as follower_router
from app.routers.chat import router as chat_router

from starlette.applications import Starlette
from starlette_admin.contrib.sqla import Admin, ModelView

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(post_router)
app.include_router(post_app)
app.include_router(profile_router)
app.include_router(like_router)
app.include_router(comment_router)
app.include_router(follower_router)
app.include_router(chat_router)

# Create admin
admin = Admin(engine, title="Social Media")

# Add view
admin.add_view(ModelView(User))
admin.add_view(ModelView(Followers))
admin.add_view(ModelView(Like))
admin.add_view(ModelView(Comment))
admin.add_view(ModelView(Post))

# Mount admin to your app
admin.mount_to(app)
