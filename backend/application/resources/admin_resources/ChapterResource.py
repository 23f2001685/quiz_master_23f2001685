from flask_restful import Resource, marshal, marshal_with, reqparse, fields
from flask_security import auth_required, roles_required
from ...data.models import Chapter
from ...data.database import db

from .QuizResource import quiz_fields


chapter_fields = {
    'id': fields.Integer,
    'subject_id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'created_at': fields.String,
    'quizzes': fields.List(fields.Nested(quiz_fields))
}


class ChapterResource(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('name', type=str, required=True, help="Name is required")
    parser.add_argument('description', type=str, required=False)
    @auth_required('token')
    @roles_required('admin')
    @marshal_with(chapter_fields)
    def get(self, subject_id, c_id=None):
        if c_id:
            chapter = Chapter.query.filter_by(subject_id=subject_id, id=c_id).first()
            if not chapter:
                return {"message": f"Chapter with ID {c_id} not found"}, 404
            return chapter
        chapters = Chapter.query.filter_by(subject_id=subject_id).all()
        return chapters

    @auth_required('token')
    @roles_required('admin')
    def post(self, subject_id):
        args = self.parser.parse_args()
        name = args.get('name')
        desc = args.get('description')

        if not subject_id:
            return {"message": "Error! Subject not found"}

        if Chapter.query.filter_by(name=name, subject_id=subject_id).first():
            return {"message": f"Chapter '{name}' already exists!"}

        new_chapter = Chapter(name=name, description=desc, subject_id=subject_id)
        db.session.add(new_chapter)
        db.session.commit()

        return marshal(new_chapter, chapter_fields)

    @auth_required('token')
    @roles_required('admin')
    def put(self, subject_id, c_id):

        args = self.parser.parse_args()
        name = args.get('name')
        desc = args.get('description')


        chapter = Chapter.query.filter_by(id=c_id, subject_id=subject_id).first()
        if not chapter:
            return {"message": f"Chapter with ID {c_id} not found"}

        chapter.name = name
        chapter.description = desc
        db.session.commit()

        return {"message": f"Chapter '{name}' updated successfully"}

    @auth_required('token')
    @roles_required('admin')
    def delete(self, subject_id, c_id):

        chapter = Chapter.query.filter_by(subject_id=subject_id, id=c_id).first()
        if not chapter:
            return {"message": f"Chapter with ID {c_id} not found"}

        db.session.delete(chapter)
        db.session.commit()

        return {"message": f"Chapter with ID {c_id} deleted successfully"}
