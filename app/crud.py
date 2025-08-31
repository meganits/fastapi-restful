from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash

# User CRUD operations
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Todo CRUD operations
def get_todos(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Todo).filter(models.Todo.owner_id == user_id).offset(skip).limit(limit).all()

def get_todo_by_id(db: Session, todo_id: int, user_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == user_id).first()

def create_user_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    db_todo = models.Todo(**todo.dict(), owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, todo_id: int, todo_update: schemas.TodoUpdate, user_id: int):
    db_todo = get_todo_by_id(db, todo_id, user_id)
    if db_todo:
        update_data = todo_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_todo, field, value)
        db.commit()
        db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int, user_id: int):
    db_todo = get_todo_by_id(db, todo_id, user_id)
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo