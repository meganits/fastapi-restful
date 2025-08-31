# fastapi-restful
restfulapi-using fastapi
A complete backend implementation built with FastAPI featuring user authentication, todo management, database migrations, and background tasks.

Features Implemented
>User authentication with JWT tokens
>Complete Todo CRUD operations
>Database migrations using Alembic
>Background tasks for email notifications
>Automated testing with pytest
>SQLite database with PostgreSQL readiness
>Environment variables configuration
>Automatic API documentation

Technology Stack
Framework: FastAPI
Database: SQLite with SQLAlchemy ORM
Authentication: JWT (JSON Web Tokens)
Migrations: Alembic
Testing: pytest
Validation: Pydantic models

Background Tasks: FastAPI BackgroundTasks

Project Structure
text
fastapi-restful/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── crud.py
│   ├── auth.py
│   └── background.py
├── tests/
│   └── test_main.py
├── alembic/
│   └── versions/
├── requirements.txt
├── .env
├── .gitignore
├── Dockerfile
└── docker-compose.yml


API Endpoints
Authentication Endpoints
POST /register - User registration
POST /token - User login and JWT token generation

Todo Endpoints (Protected)
GET /todos - Retrieve all todos for authenticated user

POST /todos - Create a new todo

PUT /todos/{id} - Update a specific todo

DELETE /todos/{id} - Delete a specific todo

Health Check
GET / - API status check

Installation and Setup
Clone the repository:

text
git clone https://github.com/meganits/fastapi-restful.git
cd fastapi-restful
Create and activate virtual environment:

text
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
Install dependencies:

text
pip install -r requirements.txt
Set up environment variables in .env file:

text
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
Run database migrations:

text
alembic upgrade head
Start the application:

text
uvicorn app.main:app --reload
Access API Documentation
After starting the application, access the interactive API documentation at:
http://localhost:8000/docs

Testing
Run the test suite with pytest:
pytest tests/test_main.py -v

Database Migrations
The application uses Alembic for database schema migrations. To create new migrations after model changes:

alembic revision --autogenerate -m "description of changes"
alembic upgrade head

Background Tasks
The implementation includes background tasks for sending email notifications when new todos are created. This runs asynchronously without blocking the main API response.


Assessment Requirements Completed
This implementation addresses all specified requirements including CRUD operations, authentication, database migrations, background tasks, and testing. The code follows proper project structure and includes comprehensive documentation.
