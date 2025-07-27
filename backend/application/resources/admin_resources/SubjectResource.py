from flask import jsonify
from flask_restful import Resource, marshal_with, reqparse, fields
from flask_security import auth_required, roles_required
from ...data.models import Subject
from ...data.database import db

from .ChapterResource import chapter_fields

subject_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'created_at': fields.String,
    'chapters': fields.List(fields.Nested(chapter_fields))
}


class SubjectResource(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('name', type=str, required=True, help="Subject name is required!")
    parser.add_argument('description', type=str, required=False)


    @auth_required('token')
    @roles_required('admin')
    @marshal_with(subject_fields)
    def get(self, subject_id=None):
        if subject_id:
            subject = Subject.query.filter(Subject.id == subject_id).first_or_404(f"Subject with subject id {subject_id} does not exist.")
            return subject
        subjects = Subject.query.all()
        return subjects, 201

    @auth_required('token')
    @roles_required('admin')
    def post(self):
        args = self.parser.parse_args()
        name = args.get('name')
        desc = args.get('description')
        # Check if subject already exists
        if Subject.query.filter_by(name=name).first():
            return {"message": f"Subject '{name}' already exists!"}, 400

        new_subject = Subject(name=name, description=desc)
        db.session.add(new_subject)
        db.session.commit()

        return {
            "id": new_subject.id,
            "name": new_subject.name,
            "description": new_subject.description,
            "created_at": new_subject.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }, 201

    @auth_required('token')
    @roles_required('admin')
    @marshal_with(subject_fields)
    def put(self, subject_id):
        subject = Subject.query.filter(Subject.id==subject_id).first()
        if not subject:
            return jsonify({
                "message": "Subject doesn't exist"
            }), 404
        args = self.parser.parse_args()
        if args['name']:
            try:
                subject.name = args.name
            except ValueError:
                return {"message": "Invalid name format."}, 400
        if args['description']:
            try:
                subject.description = args.description
            except ValueError:
                return {"message": "Invalid description format."}, 400

        db.session.commit()

        return subject


    @auth_required('token')
    @roles_required('admin')
    def delete(self, subject_id):
        sub = Subject.query.filter(Subject.id==subject_id).first()
        if not sub:
            return jsonify({
                "message": "Subject doesn't exist"
            })
        db.session.delete(sub)
        db.session.commit()
        return jsonify({"message": f"Subject {sub.name} deleted successfully"})
