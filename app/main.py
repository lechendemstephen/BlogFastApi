from fastapi import FastAPI # type: ignore
from .routers import post, users, vote
from .database import engine
from . import models
from .config import settings

Base = models.Base.metadata.create_all(bind=engine)

# creating an instance of the fastapi library
app = FastAPI()



# creating routers for various routes of the application
app.include_router(post.router)
app.include_router(users.router)
app.include_router(vote.router)


