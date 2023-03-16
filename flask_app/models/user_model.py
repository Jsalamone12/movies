from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import BCRYPT, DATABASE
from flask import flash


class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def find_one_by_username(cls, username):

        data = {
            'username' : username
        }

        query = """
        SELECT * FROM users 
        WHERE username  = %(username)s
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            return cls(results[0])
        else:
            return False
        
    @classmethod
    def find_one_by_id(cls, id):

        data = {
            'id' : id
        }

        query = """
        SELECT * FROM users 
        WHERE id  = %(id)s
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            return cls(results[0])
        else:
            return False


    @classmethod
    def create(cls, form):

       
        data = {
          **form,
          'password' : BCRYPT.generate_password_hash(form['password'])
       }
        
        query = """
        INSERT INTO users
        (username, password)
        VALUES(%(username)s, %(password)s )
        """

        return connectToMySQL(DATABASE).query_db(query, data)


    @classmethod

    def login(cls, form):

        found_user = cls.find_one_by_username(form['username'])

        if found_user:
            
            if BCRYPT.check_password_hash(found_user.password, form['password']):
                return found_user
        else:
            flash('invalid login')
            return False


    @staticmethod
    def validate(form):
        is_valid = True

        if User.find_one_by_username(form['username']):
            is_valid = False
            flash("username already exists!")

        if form['password'] != form['confirm_password']:
            is_valid = False 
            flash('passwords dont match!')
        



        return is_valid
