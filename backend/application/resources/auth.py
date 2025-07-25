from datetime import datetime
from flask import request
from flask import current_app as app
from flask_login import current_user, login_user
from flask_restful import Resource, marshal_with, reqparse, fields
from flask_security import auth_required, roles_required
from flask_security.utils import hash_password, verify_password

from ..database import db

user_fields = {
    'email': fields.String,
    'full_name': fields.String,
    'roles': fields.List(fields.String),
}

login_response_fields = {
    'message': fields.String,
    'user': fields.Nested(user_fields),
    'authentication_token': fields.String(default=None),
}

class UserRegisterResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')
        qualification = data.get('qualification')
        dob = data.get('dob')


        if not all([email, password, full_name]):
            return {'message': 'Email, password, and full name are required'}, 400
        if app.security.datastore.find_user(email=email):
            return {'message': 'User with this email already exists'}, 400

        try:
            dob_date = datetime.strptime(dob, '%Y-%m-%d').date() if dob else None

            user = app.security.datastore.create_user(
                email=email,
                password=hash_password(password),
                full_name=full_name,
                qualification=qualification,
                dob=dob_date,
                active=True
            )

            user_role = app.security.datastore.find_role('user')
            app.security.datastore.add_role_to_user(user, user_role)

            db.session.commit()
            return {'message': 'User registered successfully'}, 201
        except ValueError:
            return {'message': 'Invalid date format for dob. Use YYYY-MM-DD'}, 400
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error registering user: {str(e)}'}, 500


class UserProfileResource(Resource):
    @auth_required('token')
    @roles_required('user')
    def get(self):
        user = current_user
        return {
            'email': user.email,
            'full_name': user.full_name,
            'qualification': user.qualification,
            'dob': user.dob.isoformat() if user.dob else None,
        }, 200

    @auth_required('token')
    @roles_required('user')
    def put(self):
        data = request.get_json()
        full_name = data.get('full_name')
        qualification = data.get('qualification')
        dob = data.get('dob')
        user = current_user

        try:
            if full_name:
                user.full_name = full_name
            if qualification:
                user.qualification = qualification
            if dob:
                user.dob = datetime.strptime(dob, '%Y-%m-%d').date()

            db.session.commit()
            return {'message': 'Profile updated successfully'}, 200
        except ValueError:
            return {'message': 'Invalid date format for dob. Use YYYY-MM-DD'}, 400
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error updating profile: {str(e)}'}, 500
