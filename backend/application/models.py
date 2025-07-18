from datetime import datetime
from flask_security import UserMixin, RoleMixin
from sqlalchemy.orm import relationship

from application.database import db, Base


roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin, Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=False)
    qualification = db.Column(db.String(100))
    dob = db.Column(db.Date)

    # Flask-Security
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)

    # Relationships
    roles = relationship('Role', secondary=roles_users,
                        backref=db.backref('users', lazy='dynamic'))
    quiz_attempts = relationship('QuizAttempt', back_populates='user')

    def __repr__(self):
        return f'<User {self.email}>'


class Subject(db.Model):
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationships
    chapters = relationship('Chapter', back_populates='subject', cascade='all, delete-orphan')

class Chapter(db.Model):
    __tablename__ = 'chapters'

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)

    subject = relationship('Subject', back_populates='chapters')
    quizzes = relationship('Quiz', back_populates='chapter', cascade='all, delete-orphan')

class Quiz(db.Model):
    """
    Quiz model representing a test for a specific chapter
    """
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False)
    date_of_quiz = db.Column(db.DateTime, nullable=False)
    time_duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    remarks = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    chapter = relationship('Chapter', back_populates='quizzes')
    questions = relationship('Question', back_populates='quiz', cascade='all, delete-orphan')
    attempts = relationship('QuizAttempt', back_populates='quiz', cascade="all, delete-orphan")

class Question(db.Model):
    """
    Question model for MCQ questions in a quiz
    """
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255), nullable=False)
    option4 = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)

    # Relationships
    quiz = relationship('Quiz', back_populates='questions')

class QuizAttempt(db.Model):
    """
    Quiz attempt model to track user performance
    """
    __tablename__ = 'quiz_attempts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    total_score = db.Column(db.Float, nullable=False)
    max_score = db.Column(db.Float, nullable=False)
    percentage = db.Column(db.Float, nullable=False)

    # Relationships
    user = relationship('User', back_populates='quiz_attempts')
    quiz = relationship('Quiz', back_populates='attempts')
