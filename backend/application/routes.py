from flask import current_app as app
from flask import redirect


@app.route('/admin')
def admin():
    return "<h1> Admin Page </h1>"

@app.route('/')
def home():
    return redirect('/login')