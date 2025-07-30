from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from flask_restful import Api
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.utils import hash_password

from application.config import LocalDevConfig
from application.data import models
from application.data.database import db
from application.data.models import User, Role
from application import cache

migrate = Migrate()
cors = CORS()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevConfig)
    db.init_app(app)
    cors.init_app(app, origins=["*"], supports_credentials=True)
    migrate.init_app(app, db)
    mail.init_app(app)
    api = Api(app)
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore)
    app.app_context().push()
    cache.init_app(app)
    app.app_context().push()
    return app, api, cache

app, api, cache = create_app()


# Importing routes
from application.routes import *
from application.resources.auth import UserRegisterResource, UserProfileResource
from application.resources.admin_resources import ChapterResource, QuestionResource, QuizResource, SubjectResource, UserDeactivateResource, UserListResource
from application.resources.quiz_attempt import (
    ExportUserAttemptsResource,
    QuizAttemptResource,
    QuizAttemptsResource,
    QuizAttemptsStatsResource,
    UserQuizAttemptsResource,
    UserStatsResource
)

api.add_resource(UserRegisterResource, '/api/register')
api.add_resource(UserProfileResource, '/api/profile')
api.add_resource(UserListResource, '/api/users')
api.add_resource(UserDeactivateResource, '/api/users/<int:user_id>/deactivate')
api.add_resource(SubjectResource, '/api/subjects', '/api/subjects/<int:subject_id>')
api.add_resource(ChapterResource, '/api/subjects/<int:subject_id>/chapters', '/api/subjects/<int:subject_id>/chapters/<int:c_id>')
api.add_resource(QuizResource, '/api/quizzes', '/api/quizzes/<int:quiz_id>')
api.add_resource(QuestionResource, '/api/quizzes/<int:quiz_id>/questions', '/api/quizzes/<int:quiz_id>/questions/<int:question_id>')

api.add_resource(QuizAttemptsResource, '/api/quiz-attempts')
api.add_resource(QuizAttemptResource, '/api/quiz-attempts/<int:attempt_id>')
api.add_resource(UserQuizAttemptsResource, '/api/users/<int:user_id>/quiz-attempts')
api.add_resource(UserStatsResource, '/api/users/<int:user_id>/stats')
api.add_resource(QuizAttemptsStatsResource, '/api/quiz-attempts/stats')
api.add_resource(ExportUserAttemptsResource, '/api/quiz-attempts/export')

app.app_context().push()

if __name__ == "__main__":
    with app.app_context():
        app.security.datastore.find_or_create_role(name="admin", description="Superuser of app")
        app.security.datastore.find_or_create_role(name="user", description="General user of app")
        db.session.commit()

        if not app.security.datastore.find_user(email="admin@quizmaster.com"):
            app.security.datastore.create_user(
                email="admin@quizmaster.com",
                password = hash_password("admin@1234"),
                full_name = "Quiz Master",
                roles=['admin']
            )

        if not app.security.datastore.find_user(email="ishantkumar761@gmail.com"):
            app.security.datastore.create_user(
                email="ishantkumar761@gmail.com",
                password = hash_password("user@1234"),
                full_name = "User 1",
                roles=['user']
            )

        db.session.commit()
    app.run()
