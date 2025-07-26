from flask import request, jsonify
from flask_login import current_user
from flask_restful import fields, marshal_with, Resource
from flask_security import auth_required, roles_accepted
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from application.models import Chapter, QuizAttempt, Subject, User, Quiz, db
from application.tasks import export_user_attempts_csv

class QuizAttemptResource(Resource):
    # Individual quiz attempt

    @auth_required()
    def get(self, attempt_id):
        try:
            attempt = QuizAttempt.query.get_or_404(attempt_id)

            # Users own attempts
            user = current_user
            if user.has_role('admin') and attempt.user_id != user.id:
                return {'message': 'Access denied'}, 403

            return {
                'id': attempt.id,
                'user_id': attempt.user_id,
                'quiz_id': attempt.quiz_id,
                'timestamp': attempt.timestamp.isoformat(),
                'total_score': attempt.total_score,
                'max_score': attempt.max_score,
                'percentage': attempt.percentage,
                'user_name': attempt.user.email if attempt.user else None,
                'quiz_title': attempt.quiz.title if attempt.quiz else None
            }, 200

        except Exception as e:
            return {'message': f'Error retrieving quiz attempt: {str(e)}'}, 500


    @auth_required()
    @roles_accepted('admin')
    def delete(self, attempt_id):
        try:
            attempt = QuizAttempt.query.get_or_404(attempt_id)

            db.session.delete(attempt)
            db.session.commit()

            return {'message': 'Quiz attempt deleted successfully'}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Database error: {str(e)}'}, 500
        except Exception as e:
            return {'message': f'Error deleting quiz attempt: {str(e)}'}, 500


class QuizAttemptsResource(Resource):

    @auth_required()
    def get(self):
        try:
            user = current_user
            user_id = request.args.get('user_id', type=int)
            quiz_id = request.args.get('quiz_id', type=int)
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)

            if user.has_role('admin'):
                query = QuizAttempt.query
            else:
                # users can only see their own attempts, admin can see all
                query = QuizAttempt.query.filter_by(user_id=user.id)

            # filters
            if user_id and user.has_role('admin'):
                query = query.filter_by(user_id=user_id)
            if quiz_id:
                query = query.filter_by(quiz_id=quiz_id)
            # Ordering
            query = query.order_by(QuizAttempt.timestamp.desc())
            paginated = query.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            attempts = [{
                'id': attempt.id,
                'user_id': attempt.user_id,
                'quiz_id': attempt.quiz_id,
                'timestamp': attempt.timestamp.isoformat(),
                'total_score': attempt.total_score,
                'max_score': attempt.max_score,
                'percentage': attempt.percentage,
                'user_name': attempt.user.email if attempt.user else None,
                'quiz_title': attempt.quiz.title if attempt.quiz else None
            } for attempt in paginated.items]

            return {
                'attempts': attempts,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': paginated.total,
                    'pages': paginated.pages,
                    'has_next': paginated.has_next,
                    'has_prev': paginated.has_prev
                }
            }, 200

        except Exception as e:
            return {'message': f'Error retrieving quiz attempts: {str(e)}'}, 500

    @auth_required()
    def post(self):
        try:
            user = current_user
            data = request.get_json()

            # 1. Validate input
            if not data or 'quiz_id' not in data or 'answers' not in data:
                return {'message': 'Missing quiz_id or answers in request'}, 400

            quiz_id = data.get('quiz_id')
            user_answers = data.get('answers') # e.g., {"question_id": "selected_option"}

            # 2. Fetch the quiz and its questions from the database
            quiz = Quiz.query.options(db.joinedload(Quiz.questions)).get(quiz_id)
            if not quiz:
                return {'message': 'Quiz not found'}, 404

            if not quiz.questions:
                return {'message': 'This quiz has no questions'}, 400

            # 3. Calculate the score securely on the server
            total_score = 0
            max_score = len(quiz.questions)

            for question in quiz.questions:
                # User's answer for the current question (handle string keys from JSON)
                user_answer_str = user_answers.get(str(question.id))

                if user_answer_str is not None:
                    try:
                        user_answer_int = int(user_answer_str)
                        if user_answer_int == question.correct_option:
                            total_score += 1
                    except (ValueError, TypeError):
                        # Ignore if the answer is not a valid integer
                        continue

            percentage = (total_score / max_score) * 100 if max_score > 0 else 0

            # 5. Create and save the new QuizAttempt
            attempt = QuizAttempt(
                user_id=user.id,
                quiz_id=quiz_id,
                total_score=total_score,
                max_score=max_score,
                percentage=round(percentage, 2),
                timestamp=datetime.now()
            )

            db.session.add(attempt)
            db.session.commit()

            # 6. Return the result to the frontend
            return {
                'message': 'Quiz attempt created successfully',
                'attempt': {
                    'id': attempt.id,
                    'user_id': attempt.user_id,
                    'quiz_id': attempt.quiz_id,
                    'timestamp': attempt.timestamp.isoformat(),
                    'total_score': attempt.total_score,
                    'max_score': attempt.max_score,
                    'percentage': attempt.percentage
                }
            }, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': f'Database error: {str(e)}'}, 500
        except Exception as e:
            return {'message': f'An unexpected error occurred: {str(e)}'}, 500


class UserQuizAttemptsResource(Resource):
    # getting quiz attempts by user

    @auth_required()
    def get(self, user_id):
        # Get all quiz attempts for a user
        try:

            if current_user.has_role('admin') and current_user.id != user_id:
                return {'message': 'Access denied'}, 403

            user = User.query.get_or_404(user_id)

            # query params
            quiz_id = request.args.get('quiz_id', type=int)
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)

            query = QuizAttempt.query.filter_by(user_id=user_id)

            if quiz_id:
                query = query.filter_by(quiz_id=quiz_id)
            # Arrange according to time
            query = query.order_by(QuizAttempt.timestamp.desc())

            # Pagination
            paginated = query.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )

            attempts = [{
                'id': attempt.id,
                'quiz_id': attempt.quiz_id,
                'timestamp': attempt.timestamp.isoformat(),
                'total_score': attempt.total_score,
                'max_score': attempt.max_score,
                'percentage': attempt.percentage,
                'quiz_title': attempt.quiz.title if attempt.quiz else None
            } for attempt in paginated.items]

            return {
                'user_id': user_id,
                'user_name': user.email,
                'attempts': attempts,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': paginated.total,
                    'pages': paginated.pages,
                    'has_next': paginated.has_next,
                    'has_prev': paginated.has_prev
                }
            }, 200

        except Exception as e:
            return {'message': f'Error retrieving user quiz attempts: {str(e)}'}, 500

class UserStatsResource(Resource):
    # getting quiz attempts by user

    @auth_required()
    def get(self, user_id):
        # Get all quiz attempts for a user
        try:

            if current_user.has_role('admin') and current_user.id != user_id:
                return {'message': 'Access denied'}, 403

            user = User.query.get_or_404(user_id)

            query = QuizAttempt.query.filter_by(user_id=user_id)

            query = query.order_by(QuizAttempt.timestamp.desc())

            attempts = [{
                'id': attempt.id,
                'timestamp': attempt.timestamp.isoformat(),
                'subject_name': attempt.quiz.chapter.subject.name if attempt.quiz and attempt.quiz.chapter else None
            } for attempt in query.all()]

            return {
                'user_id': user_id,
                'user_name': user.email,
                'attempts': attempts,
            }, 200

        except Exception as e:
            return {'message': f'Error retrieving user quiz attempts: {str(e)}'}, 500


class QuizAttemptsStatsResource(Resource):
    # Stats

    @auth_required()
    @roles_accepted('admin')
    def get(self):
        try:
            # Get all quiz attempts with quiz and subject information
            attempts = db.session.query(QuizAttempt).join(Quiz).join(Chapter).join(Subject).all()

            # Calculate subject-wise top scores
            subject_top_scores = {}
            subject_attempts = {}

            for attempt in attempts:
                subject_name = attempt.quiz.chapter.subject.name

                # Track top scores per subject
                if subject_name not in subject_top_scores:
                    subject_top_scores[subject_name] = attempt.percentage
                else:
                    if attempt.percentage > subject_top_scores[subject_name]:
                        subject_top_scores[subject_name] = attempt.percentage

                # Count attempts per subject
                if subject_name not in subject_attempts:
                    subject_attempts[subject_name] = 1
                else:
                    subject_attempts[subject_name] += 1

            return {
                'subject_top_scores': subject_top_scores,
                'subject_attempts': subject_attempts,
                'total_attempts': len(attempts)
            }

        except Exception as e:
            return {'message': 'Failed to fetch stats', 'error': str(e)}, 500

class ExportUserAttemptsResource(Resource):
    @auth_required()
    def post(self):
        """Triggers a background job to export user's quiz attempts as a CSV."""
        try:
            user = current_user
            export_user_attempts_csv.delay(user.id)
            return {'message': 'Your quiz history is being exported. You will receive an email with the CSV file shortly.'}, 202
        except Exception as e:
            return {'message': f'An unexpected error occurred: {str(e)}'}, 500
