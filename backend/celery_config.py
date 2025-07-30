from celery import Celery
from celery.schedules import crontab
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
    from application.data.database import db
    db.init_app(app)

    # Initialize mail with app
    mail = Mail(app)

    # Create Celery instance
    celery = Celery('quiz_master')

    # Configure Celery
    celery.conf.update(
        broker_url='redis://localhost:6379/1',
        result_backend='redis://localhost:6379/2',
        timezone='UTC',
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        beat_schedule={
            'daily-quiz-reminders': {
                'task': 'application.tasks.send_daily_quiz_reminders',
                'schedule': crontab(hour=20, minute=0),  # Every day at 8:00 PM
                # 'schedule': '60',  # Every minute
            },
            'monthly-performance-reports': {
                'task': 'application.tasks.send_monthly_performance_reports',
                'schedule': crontab(day_of_month=1, hour=0, minute=0),  # Every month on the 1st at midnight
                # 'schedule': '120',  # Every two minutes
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
