from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user_model import User

@app.route('/')
def index():
    return redirect('/login_page')

@app.route('/login_page')
def login_page():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    # print(request.form)

    logged_in_user = User.login(request.form)

    if logged_in_user:
        session['uid'] = logged_in_user.id
        return redirect('/dashboard')


    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    print(request.form)

    if not User.validate(request.form):
        return redirect('/login_page')

    User.create(request.form)
    return redirect('/')



