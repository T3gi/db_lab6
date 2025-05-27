from fastapi import FastAPI, Depends
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

@app.post("/posts/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db=db, post=post)

@app.get("/posts/", response_model=list[schemas.Post])
def read_posts(db: Session = Depends(get_db)):
    return crud.get_posts(db)

@app.post("/comments/", response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(db=db, comment=comment)

@app.get("/comments/", response_model=list[schemas.Comment])
def read_comments(db: Session = Depends(get_db)):
    return crud.get_comments(db)

@app.on_event("startup")
def on_startup():
    seed_roles()
