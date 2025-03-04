from flask import current_app as app


@app.route('/admin')
def admin():
    return "<h1> Admin Page </h1>"