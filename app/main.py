from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi import BackgroundTasks
from .background import send_new_todo_notification
from . import models, schemas, crud
from .database import engine, get_db
from .auth import create_access_token, get_current_user, verify_password

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app with security scheme
app = FastAPI(
    title="Todo API",
    description="A simple Todo API with authentication",
    version="1.0.0",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

# Define the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication endpoints
@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.email)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Todo endpoints (protected)
@app.get("/todos", response_model=list[schemas.Todo])
def read_todos(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    todos = crud.get_todos(db, user_id=current_user.id, skip=skip, limit=limit)
    return todos

@app.post("/todos", response_model=schemas.Todo)
def create_todo(
    todo: schemas.TodoCreate,
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Create the todo first
    db_todo = crud.create_user_todo(db=db, todo=todo, user_id=current_user.id)
    
    # Add background task to send notification
    background_tasks.add_task(
        send_new_todo_notification,
        email=current_user.email,
        todo_title=todo.title
    )
    
    return db_todo

@app.put("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(
    todo_id: int,
    todo_update: schemas.TodoUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    todo = crud.update_todo(db, todo_id=todo_id, todo_update=todo_update, user_id=current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    todo = crud.delete_todo(db, todo_id=todo_id, user_id=current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}

# Health check endpoint
@app.get("/")
def read_root():
    return {"message": "Todo API is running!"}