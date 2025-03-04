from flask_security import UserMixin
from sqlalchemy.orm import relationship

from application.database import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    qualification = db.Column(db.String(100))
    dob = db.Column(db.Date)

    # Flask-Security
    active = db.Column(db.Boolean(), default=True)
    confirmed_at = db.Column(db.DateTime())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    
    # Admin boolean
    is_admin = db.Column(db.Boolean(), default=False)

    # Relationships
    quiz_attempts = relationship('QuizAttempt', back_populates='user')


