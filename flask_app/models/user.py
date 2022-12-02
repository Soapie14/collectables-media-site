# import the function that will return an instance of a connection
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import user
import re

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
DB = "project" 

class User:
    
    def __init__(self,user):

        self.id = user["id"]
        self.first_name = user["first_name"]
        self.last_name = user["last_name"]
        self.email = user["email"]
        # self.password = user['password'] if password in user else None
        self.created_at = user["created_at"]
        self.updated_at = user["updated_at"]

    @classmethod
    def get_by_email(cls,email):

        data = {
            "email": email
        }
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DB).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_by_id(cls, user_id):

        data = {"id": user_id}
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query,data)
        # Didn't find a matching user
        
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * from users;"
        user_data = connectToMySQL(DB).query_db(query)
        users = []
        for user in user_data:
            users.append(cls(user))
        return users

    @classmethod
    def create_valid_user(cls, user):
        if not cls.is_valid(user):
            return False

        pw_hash = bcrypt.generate_password_hash(user['password'])
        user = user.copy()
        user["password"] = pw_hash
        print("User after adding pw: ", user)
#after encrypting password we can now add into our database with query, we use """ so we do not have to worry about quotes being used in the query
        query = """
                INSERT into users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""

        result = connectToMySQL(DB).query_db(query, user) #result = the query adding in user information
        new_user = cls.get_by_id(result) #the result is now added through query, we can use our getbyid function to get this result

        return new_user

    @classmethod
    def existing_user_by_input(cls, user_input): #searching for existing valid user(login)
        
        valid = True
        existing_user = cls.get_by_email(user_input["email"])
        password_valid = True

        if not existing_user:
            valid = False
        else:
            password_valid = bcrypt.check_password_hash(
            existing_user.password, user_input['password'])
        
            if not password_valid:
                valid = False

        if not valid:
            flash("This does not match any of our records, please try again.", "login")
            return False

        return existing_user
    

    @classmethod
    def is_valid(cls, user):
        valid = True

        if len(user["first_name"]) < 2:
            valid = False
            flash("*First name must be at least 2 characters.", "register")
        if len(user["last_name"]) < 2:
            valid = False
            flash("*Last name must be at least 2 characters.", "register") 
        if not EMAIL_REGEX.match(user['email']): 
            valid = False
            flash("*Invalid email address!")
        if not user["password"] == user["password_confirmation"]:
            valid = False
            flash("*Passwords do not match, try again.", "register")
            
        if len(user["password"]) < 8:
            valid= False
            flash("*Make sure your password is at lest 8 letters", "password")
            
        if re.search('[0-9]',user["password"]) is None:
            valid= False
            flash("*Make sure your password has a number in it", "password")
        
        if re.search('[A-Z]',user["password"]) is None:
            valid= False
            flash("*Make sure your password has a capital letter in it", "password")
        
        email_already_has_account = User.get_by_email(user["email"])
        if email_already_has_account:
            flash("*An account with that email already exists, please log in.", "register")
            valid = False

        return valid