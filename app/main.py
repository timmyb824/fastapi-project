from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# defined schema with pydantic
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# connect to database (missing the password parameter)
while True:
    try:
        conn = psycopg2.connect(host="", database="", user="", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connected to DB!")
        break
    except Exception as error:
        print("Connection to DB failed!")
        print("Error: ", error)
        time.sleep(2)

my_posts = [{"title": "title of post 1", "content": "First post", "id": 1}, {"title": "title of post 2", "content": "second post", "id": 2}]

def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index

@app.get("/")
def root(): # "async def..." is optional if you want to use it
    return {"message": "Hello World!"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published)) # %s is a placeholder for the values; prevents SQL injection
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int): # id is a path parameter: int is the  type of the parameter using pydantic
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),)) # convert id from int to str
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id {id} not found")
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),)) # return the deleted post
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id {id} not found")
    return {"message": f"post with id {id} deleted"}

@app.put("/posts/{id}")
def update_posts(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id {id} not found")
    return {"data": updated_post}