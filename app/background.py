import logging
from fastapi import BackgroundTasks
from . import crud, models, schemas
from sqlalchemy.orm import Session

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_new_todo_notification(email: str, todo_title: str):
    """
    Simulate sending an email notification for new todo
    This runs in the background without blocking the API response
    """
    # Simulate email sending delay
    import time
    time.sleep(2)  # Simulate 2-second delay
    
    # In a real application, you would:
    # - Connect to email service (Gmail, SendGrid, etc.)
    # - Send actual email
    # - Handle errors and retries
    
    logger.info(f"📧 Email sent to {email}: New todo created - '{todo_title}'")
    print(f"📧 Email notification sent to {email} for todo: {todo_title}")