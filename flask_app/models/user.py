from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX=re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')


class User:
    
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def create_user(cls, form):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)'
        result = connectToMySQL('muro_privado').query_db(query,form)
        return result

    @classmethod
    def user_by_email(cls, form):
        query = 'SELECT * FROM users WHERE email = %(email)s'
        result = connectToMySQL('muro_privado').query_db(query, form)
        if len(result)<1:
            return False
        else:
            user=cls(result[0])
            return user
        
    @classmethod
    def user_by_id(cls, form):
        query = 'SELECT * FROM users WHERE id= %(id)s'
        result = connectToMySQL('muro_privado').query_db(query,form)
        print(result)
        user = cls(result[0])
        return user
    
    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users ORDER BY first_name ASC'
        results = connectToMySQL('muro_privado').query_db(query)
        users = []
        for user in results:
            inst_user = cls(user)
            users.append(inst_user)
        return users
    
    @staticmethod
    def validation(form):
        is_valid=True
        if len(form['first_name'])<2:
            flash('First name at least 2 characters', 'register')
            is_valid = False
        if len(form['last_name'])<2:
            flash('Last name at least 2 characeters', 'register')
            is_valid=False
        if not EMAIL_REGEX.match(form['email']):
            flash('Use a valid email address', 'register')
            is_valid=False
        query = 'SELECT * FROM users WHERE email=%(email)s'
        results = connectToMySQL('muro_privado').query_db(query, form)
        if len(results)>=1:
            flash('Email already exists', 'register')
            is_valid=False
        if not PASSWORD_REGEX.match(form['password']):
            flash('Password should be a combination of upper and lowercase letters, numbers, and special symbols.', 'register')
            is_valid=False
        if form['password']!=form['c_password']:
            flash('Passwords dont match', 'register')
            is_valid=False
        return is_valid