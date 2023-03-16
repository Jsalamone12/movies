from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.movie_model import Movie

from flask import render_template, request, redirect, session, flash

@app.route('/dashboard')
def dashboard():

    if not 'uid' in session:
        flash('please log in')
        return redirect('/')
    
    logged_in_user = User.find_one_by_id(session['uid'])

    movies = Movie.get_with_users()

    return render_template("dashboard.html", user=logged_in_user, movies=movies)

@app.route('/new_movie')
def new_movie():
    if not 'uid' in session:
        flash('please log in first')
        return redirect('/')
    
    logged_in_user = User.find_one_by_id(session['uid'])

    return render_template('new_movie.html', user=logged_in_user)

@app.route('/create_movie', methods=['POST'])
def create_movie():
    # print (request.form)
    Movie.create(request.form)
    return redirect('/dashboard')


@app.route('/edit_movie/<int:id>')
def edit_movie(id):
    if not 'uid' in session:
        flash('please log in first')
        return redirect('/')
    
    logged_in_user = User.find_one_by_id(session['uid'])

    movie = Movie.find_one_by_id(id)

    return render_template('edit_movie.html', user=logged_in_user, movie=movie)


@app.route('/delete_movie/<int:id>')
def delete_movie(id):
    Movie.delete_by_id(id)

    return redirect('/dashboard')

@app.route('/save_movie', methods=['POST'])
def save_movie():
    # print(request.form)
    Movie.save(request.form)

    return redirect('/dashboard')

