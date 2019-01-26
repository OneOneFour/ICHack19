import json
from flask import jsonify, render_template, request, redirect
from . import app, mongo_db


@app.route('/foods')
def show_foods():
    foods = mongo_db.db.foods.find({})
    return render_template("foods.html", foods=foods)


@app.route('/api/get_food/<name>', methods=['GET'])
def get_food(name):
    food = mongo_db.db.foods.find_one({'name': name})
    food.pop('_id')
    return jsonify(food)


@app.route('/set_food', methods=['POST'])
def set_food_form():
    new_food = {
        'name': request.form['name'],
        'expiry_date_min': request.form['expiry_date_min'],
        'expiry_date_max': request.form['expiry_date_max']
    }
    mongo_db.db.foods.insert(new_food)
    return redirect('/foods')


@app.route('/api/set_food/', methods=['POST'])
def set_food():
    foods = mongo_db.db.foods
    new_food = request.data
    if new_food:
        new_food_dict = json.loads(new_food)
        foods.insert(new_food_dict)
        if foods.find_one({'name': new_food_dict['name']}).count() > 0:
            return "Successfully created item"
    return "Something went wrong!"
