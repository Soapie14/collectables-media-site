from flask import Flask, render_template, session, redirect, request
from flask_app import app

from flask_app.models.user import User 
from flask_app.models.item import Item

from flask import flash


#log in page
@app.route("/")
def index():
    return render_template("login.html")

@app.route("/register_here")
def register_here():
    return render_template("register.html")

#register form
@app.route("/register", methods=["POST"])
def register():
    valid_user = User.create_valid_user(request.form)

    if not valid_user:
        return redirect("/register_here")
    
    session["user_id"] = valid_user.id
    
    return redirect("/dashboard")


#login form
@app.route("/login", methods=["POST"])
def login():
    valid_user = User.existing_user_by_input(request.form)
    if not valid_user:
        return redirect("/")
    session["user_id"] = valid_user.id
    return redirect("/dashboard")


#user dashboard
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("You must be logged in to access the dashboard.")
        return redirect("/")
    
    user = User.get_by_id(session["user_id"])
    items = Item.get_all()
    return render_template("dashboard.html", user=user, items=items) 

#may need to add (recipe=recipe) as well as user above
#not recipe but sql relationship name


#end session
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")