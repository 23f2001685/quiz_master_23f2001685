import os
from celery.schedules import crontab

class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # Celery Configuration
    broker_url = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/1'
    result_backend = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/2'
    timezone = 'UTC'
    beat_schedule = {
        'daily-quiz-reminders': {
            'task': 'application.tasks.send_daily_quiz_reminders',
            'schedule': crontab(hour=2, minute=59),
        },
        'monthly-performance-reports': {
            'task': 'application.tasks.send_monthly_performance_reports',
            'schedule': crontab(day_of_month=26, hour=2, minute=59),
        },
    }

    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    # Caching Configuration
    CACHE_TYPE = 'RedisCache'  # Use Redis for caching
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 1

class LocalDevConfig(Config):
    # Configuration
    SQLALCHEMY_DATABASE_URI = "sqlite:///quiz_master.db"
    DEBUG = True

    # Security Configurations
    SECRET_KEY = "h$5wj*!26=_10yh%ii21!^x2q=jgysn!!9+a&b(nznne0s427-"             # Hash user's creds in session
    SECURITY_PASSWORD_HASH = "bcrypt"                                             # Algo used to encrypt
    SECURITY_PASSWORD_SALT = "u(u$9-0&*!pusa#ddfltgk@or%et_!2j0#tz*m5&itx(y&+*)*" # Helps in hashing pass
    WTF_CSRF_ENABLED = False                                                      # Verification of origin of form
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    # Override for testing - run tasks more frequently
    beat_schedule = {
        'daily-quiz-reminders': {
            'task': 'application.tasks.send_daily_quiz_reminders',
            'schedule': 60.0,  # Every minute for testing
        },
        'monthly-performance-reports': {
            'task': 'application.tasks.send_monthly_performance_reports',
            'schedule': 120.0,  # Every 2 minutes for testing
        },
    }
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
