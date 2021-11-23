from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

# defined schema with pydantic
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "title of post 1", "content": "First post", "id": 1}, {"title": "title of post 2", "content": "second post", "id": 2}]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index

@app.get("/")
def root(): # "async def..." is optional if you want to use it
    return {"message": "Hello World"}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # print(post) # pydantic model
    # print(post.dict()) #pydantic model converted to dict
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 100000) # randrange assigns a random number to the id store in the dict in memory
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int): # id is a path parameter: int is the type of the parameter using pydantic
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with {id} not found")
    #     response.status_code = status.HTTP_404_NOT_FOUND # you can also set the status code like this but need to include response: Response path parameter
    #     return {"message": f"post with {id} not found"}
    return {"data": post}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.put("/posts/{id}")
def update_posts(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with {id} not found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with {id} not found")
    my_posts.remove(post)
    return {"message": f"post with {id} deleted"}
