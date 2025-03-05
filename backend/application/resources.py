from flask_restful import Resource
from flask_security import auth_required, roles_required

class TestResource(Resource):
    def get(self):
        return {"message": "This is a test!"}

class AdminOnlyAPI(Resource):
    @auth_required("token")  # Requires JWT token authentication
    @roles_required("admin")  # Only allows users with the 'admin' role
    def get(self):
        return {"message": "Welcome Admin! You have access to this API."}
