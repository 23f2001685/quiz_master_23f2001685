

from flask_restful import Resource, reqparse
from flask_security import auth_required, roles_required

from application.data.models import Quiz
from ...data.database import db


class QuizActivationResource(Resource):

    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('is_active', type=bool, required=True, help="is_active status is required")

    @auth_required('token')
    @roles_required('admin')
    def put(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": f"Quiz with ID {quiz_id} not found"}, 404

        quiz.is_active = not quiz.is_active

        db.session.commit()

        status = "activated" if quiz.is_active else "deactivated"
        return {
            "message": f"Quiz {status} successfully",
            "quiz": {
                "id": quiz.id,
                "title": quiz.title,
                "is_active": quiz.is_active
            }
        }, 200
