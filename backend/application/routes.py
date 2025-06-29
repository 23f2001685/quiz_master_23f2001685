from flask import current_app as app
from flask import jsonify
from flask_security import auth_required, roles_required, current_user


@app.route('/admin')
@auth_required('token')
@roles_required('admin')
def admin():
    return jsonify({
        "message" : "Admin logged in successfully."
    })

@app.route('/user')
@auth_required('token')
@roles_required('user')
def user_home():
    user = current_user
    if not user:
        return jsonify({
            "message" : "wrong user id provided"
        })

    return jsonify({
        "full_name": user.full_name,
        "email": user.email,
        "dob": user.dob
    })

@app.route('/me', methods=['GET'])
@auth_required('token')
def get_current_user():
    if not current_user.is_authenticated:
        return jsonify({"message": "User is not authenticated"}), 401

    return jsonify({
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "roles": [role.name for role in current_user.roles],
        "active": current_user.active,
    }), 200
