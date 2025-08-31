import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test tables
Base.metadata.create_all(bind=engine)

# Override get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Todo API is running!"}

def test_register_user():
    """Test user registration"""
    response = client.post(
        "/register",
        json={"email": "testuser@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "email" in response.json()
    assert response.json()["email"] == "testuser@example.com"

def test_login_user():
    """Test user login and token generation"""
    # First register
    client.post(
        "/register",
        json={"email": "loginuser@example.com", "password": "testpassword"}
    )
    
    # Then login
    response = client.post(
        "/token",
        json={"email": "loginuser@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_protected_endpoint_without_token():
    """Test that protected endpoints require authentication"""
    response = client.get("/todos")
    assert response.status_code == 401  # Unauthorized

# Add this at the end of the file
if __name__ == "__main__":
    pytest.main([__file__, "-v"])