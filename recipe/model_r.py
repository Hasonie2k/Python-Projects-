from mysqlconnection import connectToMySQL
from flask import flash
import re


class Recipe:
    def __init__(self, data):
        self.users_id = data['users_id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.date_cooked = data['date_cooked']
        self.under = data['under']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes.recipe;"
        results = connectToMySQL('recipe').query_db(query)
        recipes= []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes
    
    
    @classmethod
    def get_by_name(cls , name):
        query = "SELECT * FROM recipes.recipe WHERE name = %(name)s"
        data = {'name':name}
        result = connectToMySQL('recipes').query_db(query, data)
        if len(result)> 0 :
            return cls(result[0])
        else:
            return None
        
    @classmethod
    def get_by_id(cls, users_id):
        query = "SELECT * FROM recipes.recipe WHERE users_id = %(users_id)s"
        data = {'users_id': users_id}
        result = connectToMySQL('recipes').query_db(query, data)
        if result and len(result) > 0:
            return cls(result[0])
        else:
            return None 
    
    @classmethod
    def save_recipe(cls,data):
        query = "INSERT INTO recipes.recipe (name , description ,instruction ,users_id , date_cooked , under )VALUES (%(name)s , %(description)s, %(instruction)s , %(users_id)s , %(date_cooked)s , %(under)s)"
        return connectToMySQL('recipes').query_db(query, data)
    
    @classmethod
    def delete_recipe_by_id(cls, users_id):
        query = "DELETE FROM recipes.recipe WHERE users_id = %(users_id)s"
        data = {'users_id': users_id}
        connectToMySQL('recipes').query_db(query, data)
        
    @classmethod
    def update_recipe_by_id(cls,users_id, data):
        query = "UPDATE recipes.recipe SET name=%(name)s, description=%(description)s, instruction=%(instruction)s,under=%(under)s, date_cooked=%(date_cooked)s WHERE users_id=%(users_id)s"
        mysql = connectToMySQL('recipes')
        result = mysql.query_db(query, data)
        return result


    @staticmethod
    def validate_recipe(form_data):
        is_valid = True
        if len(form_data['name']) < 2:
            flash('name must be more than 2 characters long.')
            is_valid = False
        if len(form_data['description']) < 2:
            flash('description must be more than 2 characters long.')
            is_valid = False
        if len(form_data['instruction']) < 5:
            flash('instruction must be at least 5 characters long.')
            is_valid = False
        return is_valid
