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

