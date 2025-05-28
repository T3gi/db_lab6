from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, SessionLocal, Base
from sqlalchemy.dialects.mysql import insert

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def seed_roles():
    db = SessionLocal()
    try:
        stmt = insert(models.Role).values([
            {"name": "user"},
            {"name": "admin"}
        ])
        stmt = stmt.on_duplicate_key_update(name=stmt.inserted.name)
        db.execute(stmt)
        db.commit()
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}

@app.post("/posts/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db=db, post=post)

@app.get("/posts/", response_model=list[schemas.Post])
def read_posts(db: Session = Depends(get_db)):
    return crud.get_posts(db)

@app.get("/posts/{post_id}", response_model=schemas.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@app.put("/posts/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)):
    db_post = crud.update_post(db, post_id, post)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.delete_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"detail": "Post deleted"}

@app.post("/comments/", response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(db=db, comment=comment)

@app.get("/comments/", response_model=list[schemas.Comment])
def read_comments(db: Session = Depends(get_db)):
    return crud.get_comments(db)

@app.get("/comments/{comment_id}", response_model=schemas.Comment)
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = crud.get_comment(db, comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

@app.put("/comments/{comment_id}", response_model=schemas.Comment)
def update_comment(comment_id: int, comment: schemas.CommentUpdate, db: Session = Depends(get_db)):
    db_comment = crud.update_comment(db, comment_id, comment)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = crud.delete_comment(db, comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"detail": "Comment deleted"}

@app.on_event("startup")
def on_startup():
    seed_roles()
