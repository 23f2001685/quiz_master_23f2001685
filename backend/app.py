from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_security import Security, SQLAlchemyUserDatastore

from application.config import LocalDevConfig
from application.database import db
from application.models import User

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevConfig)
    db.init_app(app)
    migrate.init_app(app)
    api = Api(app)
    datastore = SQLAlchemyUserDatastore(db, User, None)
    app.security = Security(app, datastore)
        
    app.app_context().push()
    return app, api

app, api = create_app()
CORS(app)
# Importing routes
from application.routes import *

from application.resources import TestResource
api.add_resource(TestResource, "/test-api")

app.app_context().push()

if __name__ == "__main__":
    app.run()
