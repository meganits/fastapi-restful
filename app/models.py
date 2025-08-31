from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with todos
    todos = relationship("Todo", back_populates="owner")

class Todo(Base):  # CHANGED FROM Post to Todo
    __tablename__ = "todos"  # CHANGED FROM posts to todos
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, default="")
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with user
    owner = relationship("User", back_populates="todos")