from fastapi import FastAPI, Response, status, HTTPException, Depends
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        # Last argument simply makes sure that when we make a query we're gonna get the values with the columns names
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Database',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor() # The cursor object makes the SQL queries
        print("Database connection was successful!")
        break
    except Exception as e:
        print(f"Database connection failed: {str(e)}")
        time.sleep(2)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # Kind of equivalent to SQL's 'RETURNING *' . refresh returns the new post and stores it in new_post
    return new_post

@app.get("/posts/{id}", response_model=schemas.Post) #The client specifies the exact id he wants. The id is a path parameter.
async def get_post(id: int, db: Session = Depends(get_db)): #The function has access to the id the client sends.
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # Filter is like WHERE in SQL
    # first() is used instead of all(). all() continues to look even after finding the first one.
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} doesn't exist")

    post_query.delete(synchronize_session=False) # False is probably the default
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} doesn't exist")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hashing the password
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Kind of equivalent to SQL's 'RETURNING *' . refresh returns the new user and stores it in new_user
    return new_user

@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} doesn't exist")

    return user