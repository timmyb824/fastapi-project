from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

# tags allow you to group related endpoints together for swagger documentation
router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# get posts
@router.get("/", response_model=List[schemas.Post])
# Depends is a decorator that allows you to inject a dependency
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # get all posts for all users
    posts = db.query(models.Post).all()

    # return only the posts that belong to the current user
    # posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()

    return posts

# create a new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # print(current_user.email)
    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # refresh the new_post object and return it
    return new_post

# get a single post
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): # id is a path parameter: int is the  type of the parameter using pydantic
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id {id} not found")

    # return post only if it belongs to the current user
    # if post.user_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail= f"post not owned by current user")

    return post

# delete a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id {id} not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail= f"post not owned by current user")

    post_query.delete(synchronize_session=False)
    db.commit()
    return {"message": f"post with id {id} deleted"}

# update a post
@router.put("/{id}", response_model=schemas.Post)
def update_posts(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id {id} not found")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail= f"post not owned by current user")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()