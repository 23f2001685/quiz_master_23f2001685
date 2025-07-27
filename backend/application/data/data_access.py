from sqlalchemy.orm import joinedload, selectinload

from application.data.models import Chapter, QuizAttempt, Role, roles_users, User, Quiz, db
from application import cache


@cache.cached(timeout=60, query_string=True)
def get_quiz_attempt_by_id(attempt_id):
    """Fetch a quiz attempt by its ID."""
    return QuizAttempt.query.get_or_404(attempt_id)

@cache.cached(timeout=60, query_string=True)
def get_all_quiz_attempts():
    """Fetch all quiz attempts."""
    return QuizAttempt.query.all()

@cache.cached(timeout=60, query_string=True)
def get_quiz_attempts_by_user(user_id):
    """Fetch all quiz attempts for a specific user."""
    return QuizAttempt.query.filter_by(user_id=user_id).all()

@cache.cached(timeout=60, query_string=True)
def get_quiz_attempts_by_user_ordered_by_timestamp_desc(user_id):
    """Fetch all quiz attempts for a specific user."""
    return (
        QuizAttempt.query.options(
            joinedload(QuizAttempt.quiz).joinedload(Quiz.chapter).joinedload(Chapter.subject)
        )
        .filter_by(user_id=user_id)
        .order_by(QuizAttempt.timestamp.desc())
        .all()
    )

@cache.cached(timeout=300)
def get_quiz_attempts_with_everything():
    """Fetch statistics for all quiz attempts."""
    return (
        QuizAttempt.query.options(
                joinedload(QuizAttempt.quiz)
                .joinedload(Quiz.chapter)
                .joinedload(Chapter.subject)
            ).all()
    )

@cache.cached(timeout=60, query_string=True)
def get_all_users():
    """Fetch all users."""
    return User.query.options(selectinload(User.roles)).join(roles_users).join(Role).filter(Role.name == 'user').all()
