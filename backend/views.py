from flask import jsonify,render_template
from . import app, mongo_db


@app.route('/foods')
def show_foods():
    foods = mongo_db.db.foods.find({})
    return render_template("foods.html",foods = foods)


@app.route('/api/get_food/<name>',methods=['GET'])
def get_food(name):
    food = mongo_db.db.foods.find_one({'name': name})
    food.pop('_id')
    return jsonify(food)


@app.route('/api/set_food/',methods=['POST'])
def set_food():
    foods = mongo_db.db.foods
    new_food = {
        'name': "Cake",
        'expiry_date_min': 2,
        'expiry_date_max': 3
    }
    foods.insert(new_food)
    return "added item"
