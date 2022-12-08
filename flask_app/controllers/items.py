from flask import Flask, render_template, session, redirect, request
from flask_app import app

from flask_app.models.user import User 
from flask_app.models.item import Item

from flask import flash


#create new entry
@app.route("/create")
def create():
    if "user_id" not in session:
        flash("You must be logged in to create.")
        return redirect("/")
    
    user = User.get_by_id(session["user_id"])
    #need to add get all 
    return render_template("create.html")


@app.route("/create/new", methods=["POST"])
def create_item():
    valid_item = Item.create_valid_item(request.form)
    if valid_item:
        return redirect(f'/items/{valid_item.id}')
    return redirect('/create')

#view entry by id
@app.route("/items/<int:item_id>")
def item_detail(item_id):
    user = User.get_by_id(session["user_id"])
    item = Item.get_by_id(item_id)
    return render_template("view.html", user=user, item=item)
#may need to add similar to recipe=recipe after user=user

@app.route("/items/edit/<int:item_id>")
def item_edit_page(item_id):
    item = item.get_by_id(item_id)
    return render_template("edit.html", item=item)

@app.route("/items/<int:item_id>", methods=["POST"])
def update_item(item_id):

    valid_item = Item.update_item(request.form, session["user_id"])

    if not valid_item:
        return redirect(f"/items/edit/{item_id}")
        
    return redirect(f"/items/{item_id}")

@app.route("/items/delete/<int:item_id>")
def delete_by_id(item_id):
    Item.delete_item_by_id(item_id)
    return redirect("/dashboard")