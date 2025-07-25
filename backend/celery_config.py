from celery import Celery
from flask import Flask
from flask_mail import Mail
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_celery_app():
    # Create Flask app
    app = Flask(__name__)

    # Load configuration
    from application.config import LocalDevConfig
    app.config.from_object(LocalDevConfig)

    # Initialize database with app
    from application.database import db
    db.init_app(app)

    # Initialize mail with app
    mail = Mail(app)

    # Create Celery instance
    celery = Celery('quiz_master')

    # Configure Celery
    celery.conf.update(
        broker_url='redis://localhost:6379/0',
        result_backend='redis://localhost:6379/0',
        timezone='UTC',
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        beat_schedule={
            'daily-quiz-reminders': {
                'task': 'application.tasks.send_daily_quiz_reminders',
                'schedule': 60.0,  # Every minute for testing
            },
            'monthly-performance-reports': {
                'task': 'application.tasks.send_monthly_performance_reports',
                'schedule': 120.0,  # Every 2 minutes for testing
            },
        },
        beat_scheduler='celery.beat:PersistentScheduler',
        beat_schedule_filename='beat-schedule.db',
    )

    # Context task that properly initializes Flask app context
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery, app

# Create instances
celery_app, flask_app = create_celery_app()

# Import tasks after celery_app is created
from application import tasks
