from flask_restful import Resource, marshal_with, reqparse, fields
from flask_security import auth_required, roles_required
from ...data.models import Question, Quiz
from ...data.database import db

question_fields = {
    "id": fields.Integer,
    "quiz_id": fields.Integer,
    "question_statement": fields.String,
    "option1": fields.String,
    "option2": fields.String,
    "option3": fields.String,
    "option4": fields.String,
    "correct_option": fields.Integer,
}


class QuestionResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('quiz_id', type=int, required=True, help="Quiz ID is required")
        self.parser.add_argument('question_statement', type=str, required=True, help="Question statement is required")
        self.parser.add_argument('option1', type=str, required=True, help="Option 1 is required")
        self.parser.add_argument('option2', type=str, required=True, help="Option 2 is required")
        self.parser.add_argument('option3', type=str, required=True, help="Option 3 is required")
        self.parser.add_argument('option4', type=str, required=True, help="Option 4 is required")
        self.parser.add_argument('correct_option', type=int, required=True, help="Correct option is required (1-4)")

    @auth_required('token')
    @roles_required('admin')
    @marshal_with(question_fields)
    def get(self, quiz_id=None, question_id=None):
        if not quiz_id:
            return {"message": "Quiz ID is required"}, 400

        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": f"Quiz with ID {quiz_id} not found"}, 404

        if question_id:
            question = Question.query.filter_by(id=question_id, quiz_id=quiz_id).first()
            if not question:
                return {"message": f"Question with ID {question_id} not found in quiz {quiz_id}"}, 404
            return question

        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        return questions

    @auth_required('token')
    @roles_required('admin')
    @marshal_with(question_fields)
    def post(self, quiz_id):
        args = self.parser.parse_args()

        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": f"Quiz with ID {quiz_id} not found"}, 404

        if args['correct_option'] not in [1, 2, 3, 4]:
            return {"message": "Correct option must be between 1 and 4"}, 400

        new_question = Question(
            quiz_id=quiz_id,
            question_statement=args['question_statement'],
            option1=args['option1'],
            option2=args['option2'],
            option3=args['option3'],
            option4=args['option4'],
            correct_option=args['correct_option'],
        )

        db.session.add(new_question)
        db.session.commit()
        return new_question, 201

    @auth_required('token')
    @roles_required('admin')
    @marshal_with(question_fields)
    def put(self, quiz_id, question_id):
        args = self.parser.parse_args()

        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": f"Quiz with ID {quiz_id} not found"}, 404

        question = Question.query.filter_by(id=question_id, quiz_id=quiz_id).first()
        if not question:
            return {"message": f"Question with ID {question_id} not found in quiz {quiz_id}"}, 404

        if args['correct_option'] not in [1, 2, 3, 4]:
            return {"message": "Correct option must be between 1 and 4"}, 400

        question.question_statement = args['question_statement']
        question.option1 = args['option1']
        question.option2 = args['option2']
        question.option3 = args['option3']
        question.option4 = args['option4']
        question.correct_option = args['correct_option']

        db.session.commit()
        return question

    @auth_required('token')
    @roles_required('admin')
    def delete(self, quiz_id, question_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": f"Quiz with ID {quiz_id} not found"}, 404

        question = Question.query.filter_by(id=question_id, quiz_id=quiz_id).first()
        if not question:
            return {"message": f"Question with ID {question_id} not found in quiz {quiz_id}"}, 404

        db.session.delete(question)
        db.session.commit()
        return {"message": f"Question with ID {question_id} deleted successfully"}, 200
