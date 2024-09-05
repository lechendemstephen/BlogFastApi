from fastapi import FastAPI # type: ignore
from .routers import post, users
from .database import engine
from . import models

Base = models.Base.metadata.create_all(bind=engine)

# creating an instance of the fastapi library
app = FastAPI()



# creating routers for various routes of the application
app.include_router(post.router)
app.include_router(users.router)


