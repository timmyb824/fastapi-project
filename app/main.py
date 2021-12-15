from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from . import models
from .database import engine
from .routers import post, user, auth, vote

from fastapi.middleware.cors import CORSMiddleware


# creates the tables in the database; if they already exist, it does nothing
# commented out due to us using alembic instead
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# List of domains that can talk to our API
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # allow certain methods
    allow_headers=["*"], # allow certain headers
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# root
@app.get("/")
def root(): # "async def..." is optional if you want to use it
    return {"message": "Welcome to my first API!"}


