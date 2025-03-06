from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_security import Security, SQLAlchemyUserDatastore, hash_password

from application.config import LocalDevConfig
from application.database import db
from application.models import User, Role

migrate = Migrate()
cors = CORS()

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevConfig)
    db.init_app(app)
    cors.init_app(app)
    migrate.init_app(app, db)
    api = Api(app)
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore)
        
    app.app_context().push()
    return app, api

app, api = create_app()

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

    if not app.security.datastore.find_user(email="user1@somemail.com"):
        app.security.datastore.create_user(
            email="user1@somemail.com",
            password = hash_password("user@1234"),
            full_name = "User 1",
            roles=['user']
        )
    
    db.session.commit()


# Importing routes
from application.routes import *

from application.resources import TestResource
api.add_resource(TestResource, "/test-api")

app.app_context().push()

if __name__ == "__main__":
    app.run()
