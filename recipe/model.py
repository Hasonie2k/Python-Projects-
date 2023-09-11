from mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes.users;"
        results = connectToMySQL('recipes').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
    
    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM recipes.users WHERE email = %(email)s"
        data = {'email': email}
        result = connectToMySQL('recipes').query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None
    
    @classmethod
    def get_by_id(cls, user_id):
        query = "SELECT * FROM recipes.users WHERE id = %(user_id)s"
        data = {'user_id': user_id}
        result = connectToMySQL('recipes').query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None

    @classmethod
    def save_user(cls, data):
        query = "INSERT INTO recipes.users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL('recipes').query_db(query, data)

    @staticmethod
    def validate_user(form_data):
        is_valid = True
        if len(form_data['first_name']) < 2:
            flash('First name must be more than 2 characters long.')
            is_valid = False
        if len(form_data['last_name']) < 2:
            flash('Last name must be more than 2 characters long.')
            is_valid = False
        if not EMAIL_REGEX.match(form_data['email']):
            flash('Invalid email address.')
            is_valid = False
        if len(form_data['password']) < 5:
            flash('Password must be at least 5 characters long.')
            is_valid = False
        if form_data['confirm_password'] != form_data['password']:
            flash('Passwords must match.')
            is_valid = False
        return is_valid


