from flask_app.config.mysqlconnection import connectToMySQL
from flask import session 
from flask_app.models.user_model import User
from flask_app import DATABASE

class Movie:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.year = data['year']
        self.description = data['description']
        self.director = data['director']
        self.genre = data['genre']
        self.title_image = data['title_image']
        self.created_at = data['created_at'] 
        self.updated_at = data ['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def create(cls, form):

        data= {
            **form,
            'user_id' : session['uid']
        }

        query = """
        INSERT INTO movies
        (
            title,
            year,
            description,
            director,
            genre,
            title_image,
            user_id
        )

        VALUES(
            %(title)s,
            %(year)s,
            %(description)s,
            %(director)s,
            %(genre)s,
            %(title_image)s,
            %(user_id)s
        )
        """

        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_with_users(cls):

        query = """
        SELECT * FROM movies 
        JOIN users ON users.id=movies.user_id;
"""

        results = connectToMySQL(DATABASE).query_db(query)

        movies = []
        for result in results:
            movie = cls(result)

            user_data = {
                **result,
                'id' : result['users.id'],
                'created_at' : result['users.created_at'],
                'updated_at' : result['users.updated_at']
            }


            movie.user = User(user_data)
            movies.append(movie)

        return movies


    @classmethod
    def find_one_by_id(cls, id):

        data = {
            'id' : id
        }

        query = """
        SELECT * FROM movies 
        WHERE id  = %(id)s
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            return cls(results[0])
        else:
            return False
        

    @classmethod
    def delete_by_id(cls, id):

        data = {
            'id' : id
        }

        query = """
        DELETE FROM movies WHERE id = %(id)s
        """

        return  connectToMySQL(DATABASE).query_db(query, data)
    @classmethod
    def save(cls, data):

        query = """
            UPDATE movies SET 
            title = %(title)s,
            description = %(description)s,
            year = %(year)s,
            director = %(director)s,
            genre = %(genre)s,
            title_image = %(title_image)s
            WHERE id = %(id)s


        """
        return  connectToMySQL(DATABASE).query_db(query, data)