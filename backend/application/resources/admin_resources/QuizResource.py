from datetime import datetime
from flask_restful import Resource, marshal, marshal_with, reqparse, fields
from flask_security import auth_required, roles_required, roles_accepted
from sqlalchemy.orm import joinedload
from ...data.models import Chapter, Quiz
from ...data.database import db
from .QuestionResource import question_fields


quiz_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "chapter": fields.String(attribute="chapter.name"),
    "subject": fields.String(attribute="chapter.subject.name"),
    "date_of_quiz": fields.String(),
    "time_duration": fields.Integer,
    "remarks": fields.String,
    "is_active": fields.Boolean,
    "questions": fields.List(fields.Nested(question_fields)),
}


class QuizResource(Resource):

    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('title', type=str, required=True, help="Title is required")
    parser.add_argument('chapter_id', type=int, required=True, help="Chapter ID is required")
    parser.add_argument('date_of_quiz', type=str, required=True, help="Date of quiz is required (format: YYYY-MM-DDTHH:MM)")
    parser.add_argument('time_duration', type=int, required=True, help="Time duration (in minutes) is required")
    parser.add_argument('remarks', type=str)
    parser.add_argument('is_active', type=bool)

    @auth_required('token')
    @roles_accepted('admin', 'user')
    def get(self, quiz_id=None):
        if quiz_id:
            quiz = Quiz.query.options(
                joinedload(Quiz.chapter).joinedload(Chapter.subject),
                joinedload(Quiz.questions)
            ).get(quiz_id)
            if not quiz:
                return {"message": f"Quiz with ID {quiz_id} not found"}, 404
            return marshal(quiz, quiz_fields)

        quizzes = Quiz.query.options(
            joinedload(Quiz.chapter).joinedload(Chapter.subject),
            joinedload(Quiz.questions)
        ).all()
        return marshal(quizzes, quiz_fields), 200

    @auth_required('token')
    @roles_required('admin')
    def post(self):

        args = self.parser.parse_args()
        title = args['title']
        if not title:
            return {"message": "Title is required"}, 400
        chapter_id = args['chapter_id']
        date_of_quiz = args['date_of_quiz']
        time_duration = args['time_duration']
        remarks = args.get('remarks')
        is_active = args.get('is_active', True)

        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {"message": f"Chapter with ID {chapter_id} not found"}, 404

        try:
            print(f"Parsing date_of_quiz: {date_of_quiz}")
            # Expecting date_of_quiz in format 'YYYY-MM-DDTHH:MM'
            date_of_quiz = datetime.strptime(date_of_quiz, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            return {"message": "Invalid date format. Use YYYY-MM-DD."}, 400

        new_quiz = Quiz(
            title=title,
            chapter_id=chapter_id,
            date_of_quiz=date_of_quiz,
            time_duration=time_duration,
            remarks=remarks,
            is_active=is_active,
        )

        db.session.add(new_quiz)
        db.session.commit()
        return marshal(new_quiz, quiz_fields), 201

    @auth_required('token')
    @roles_required('admin')
    def put(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": f"Quiz with ID {quiz_id} not found"}, 404

        args = self.parser.parse_args()
        if args['title']:
            quiz.title = args['title']

        if args['chapter_id']:
            chapter = Chapter.query.get(args['chapter_id'])
            if not chapter:
                return {"message": f"Chapter with ID {args['chapter_id']} not found"}, 404
            quiz.chapter_id = args['chapter_id']
        if args['date_of_quiz']:
            try:
                quiz.date_of_quiz = datetime.strptime(args['date_of_quiz'], '%Y-%m-%dT%H:%M:%S.%fZ')
            except ValueError:
                # Fallback for format without milliseconds
                try:
                    quiz.date_of_quiz = datetime.strptime(args['date_of_quiz'], '%Y-%m-%dT%H:%M')
                except ValueError:
                    return {"message": "Invalid date format. Use YYYY-MM-DDTHH:MM or ISO format."}, 400

        if args['time_duration']:
            quiz.time_duration = args['time_duration']

        if args['remarks'] is not None:
            quiz.remarks = args['remarks']

        if args['is_active'] is not None:
            quiz.is_active = args['is_active']

        db.session.commit()

        return {
            "message": "Quiz updated successfully",
            "quiz": self.serialize_quiz(quiz)
        }, 200

    @auth_required('token')
    @roles_required('admin')
    def delete(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": f"Quiz with ID {quiz_id} not found"}, 404

        db.session.delete(quiz)
        db.session.commit()

        return {"message": f"Quiz with ID {quiz_id} deleted successfully"}, 200

    def serialize_quiz(self, quiz):
        return {
            "id": quiz.id,
            "chapter": quiz.chapter.name,
            "date_of_quiz": quiz.date_of_quiz.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
            "time_duration": quiz.time_duration,
            "remarks": quiz.remarks,
            "is_active": quiz.is_active
        }
