import json
from bson import json_util
from flask import render_template, request, redirect, abort, url_for
from . import app, mongo_db
from .models import Food


@app.route('/foods')
def show_foods():
    foods = Food.objects
    return render_template("foods.html", foods=foods)


@app.route('/api/delete_food/<id>')
def delete_food(id):
    Food.objects(id=id).delete()
    if Food.objects(id=id).count() == 0:
        return "Item deleted successfully"
    else:
        return f"Error deleting item with id:{id}"


@app.route('/api/get_food/<name>', methods=['GET'])
def get_food(name):
    food = Food.objects(name=name)
    if food:
        return food.to_json()
    else:
        return abort(404)


@app.route('/set_food', methods=['POST'])
def set_food_form():
    new_food = Food(name=request.form['name'], expiry=request.form['expiration_date'])
    new_food.save()
    return redirect('/foods')


@app.route('/api/set_food/', methods=['POST'])
def set_food():
    if request.data:
        new_food_dict = json.loads(request.data)
        new_food = Food(name = new_food_dict['name'],expiry=new_food_dict['expiry'])
        new_food.save()
        if Food.objects(id = new_food.id).count() > 0:
            return "Successfully created item"
    return abort(500)



@app.route('/login')
def show_login():
    return render_template("login.html")
