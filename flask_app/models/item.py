# import the function that will return an instance of a connection
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models import user
import re

DB = "beltexam" 

class Item:
    def __init__(self, item):
        self.id= item["id"]
        self.location= item["location"]
        self.description= item["description"]
        self.date= item["date"]
        self.amount= item["amount"]
        self.user = None
        
    #create new valid item
    @classmethod
    def create_valid_item(cls, item_dict):
        if not cls.is_valid(item_dict):
            return False
        
                
        query = """INSERT INTO items (location, description, date, amount, user_id) VALUES (%(location)s, %(description)s, %(date)s, %(amount)s, %(user_id)s);"""
        item_id = connectToMySQL(DB).query_db(query, item_dict)
        item = cls.get_by_id(item_id)

        return item
        
    #getting by id
    @classmethod
    def get_by_id(cls, item_id):
        print(f"get item by id {item_id}")
        data = {"id": item_id}
        query = """SELECT items.id, items.created_at, items.updated_at, location, description, date, amount,
                    users.id as user_id, first_name, last_name, email, users.created_at as uc, users.updated_at as uu
                    FROM items
                    JOIN users on users.id = items.user_id
                    WHERE items.id = %(id)s;"""
        
        result = connectToMySQL(DB).query_db(query,data)
        print("result of query:")
        print(result)
        result = result[0]
        item = cls(result)
        
        # convert joined user data into a user object
        item.user = user.User(
                {
                    "id": result["user_id"],
                    "first_name": result["first_name"],
                    "last_name": result["last_name"],
                    "email": result["email"],
                    "created_at": result["uc"],
                    "updated_at": result["uu"]
                }
            )

        return item
    
    
    @classmethod
    def get_all(cls):
        # Get all items, and the user info for the creators
        query = """SELECT 
                    items.id, items.created_at, items.updated_at, location, description, date, amount,
                    users.id as user_id, first_name, last_name, email, users.created_at as uc, users.updated_at as uu
                    FROM items
                    JOIN users on users.id = items.user_id;"""
        item_data = connectToMySQL(DB).query_db(query)

        # Make a list to hold item objects to return
        items = []

        # Iterate through the list of item dictionaries
        for item in item_data:

            # convert data into a item object
            item_obj = cls(item)

            # convert joined user data into a user object
            item_obj.user = user.User(
                {
                    "id": item["user_id"],
                    "first_name": item["first_name"],
                    "last_name": item["last_name"],
                    "email": item["email"],
                    "created_at": item["uc"],
                    "updated_at": item["uu"]
                }
            )
            items.append(item_obj)


        return items
    
    
    @classmethod
    def update_item(cls, item_dict, session_id):

        # Authenticate User first
        item = cls.get_by_id(item_dict["id"])
        if item.user.id != session_id:
            flash("You must be the creator to update this item.")
            return False

        # Validate the input
        if not cls.is_valid(item_dict):
            return False
        
        # Update the data in the database.
        query = """UPDATE items
                    SET location = %(location)s, description = %(description)s, date=%(date)s, amount = %(amount)s
                    WHERE id = %(id)s;"""
        result = connectToMySQL(DB).query_db(query,item_dict)
        item = cls.get_by_id(item_dict["id"])
        
        return item
    
    
    @classmethod
    def delete_item_by_id(cls, item_id):

        data = {"id": item_id}
        query = "DELETE from items WHERE id = %(id)s;"
        connectToMySQL(DB).query_db(query,data)

        return item_id
    
    @staticmethod
    def is_valid(item_dict):
        valid = True
        flash_string = " field is required and must be at least 3 characters."
        if len(item_dict["location"]) < 3:
            flash("location " + flash_string)
            valid = False
        if len(item_dict["description"]) < 3:
            flash("Description " + flash_string)
            valid = False

        if len(item_dict["date"]) <= 0:
            flash("Date is required.")
            valid = False
            
        if len(item_dict["amount"]) <= 0:
            flash("Did you actually see a sasquatch? How many?")
            valid = False

        return valid