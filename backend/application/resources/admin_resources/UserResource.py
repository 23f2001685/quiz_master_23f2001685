from flask_restful import Resource
from flask_security import auth_required, roles_required
from ...models import Role, User, roles_users
from ...database import db


class UserListResource(Resource):
    @auth_required('token')
    @roles_required('admin')
    def get(self):
        users = User.query.join(roles_users).join(Role).filter(Role.name == 'user').all()
        return [{
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            'qualification': user.qualification,
            'dob': user.dob.isoformat() if user.dob else None,
            'active': user.active,
            'roles': [role.name for role in user.roles]
        } for user in users], 200


class UserDeactivateResource(Resource):
    @auth_required('token')
    @roles_required('admin')
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        if 'user' not in [role.name for role in user.roles]:
            return {'message': 'User does not have the "user" role'}, 400
        user.active = not user.active
        db.session.commit()
        return {'message': f'User {user.email} deactivated successfully'}, 200
