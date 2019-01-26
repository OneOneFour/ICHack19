import json
from bson import json_util
from flask import render_template, request, redirect, abort, jsonify, url_for
from . import app, mongo_db
from .models import Food


@app.route('/foods')
def show_foods():
    foods = Food.objects
    return render_template("foods.html", foods=foods)


@app.route('/api/delete_food/<id>')
def delete_food(id):
    Food.objects.get_or_404(_id=id)
    if Food.objects(_id=id).count() == 0:
        return "Item deleted successfully"
    else:
        return f"Error deleting item with id:{id}"


@app.route('/api/food/<name>', methods=['GET'])
def get_food(name):
    food = Food.objects.get_or_404(name=name)
    if food:
        return food.to_json()
    else:
        return abort(404)


@app.route('/api/food/<name>/recipes', methods=['GET'])
def get_recipe_for_food(name):
    food = Food.objects.get_or_404(name=name)
    if food:
        return jsonify(food.get_recipe())
    else:
        return abort(404)


@app.route("/api/food/remove/", method=["POST"])
def remove_food_from_db():
    delete_food_dict = json.loads(request.data)
    food = Food.objects.get_or_404(_id=delete_food_dict["id"])
    food.delete()
    if Food.objects(_id=delete_food_dict["id"]).count() == 0:
        return jsonify({'result': 1})
    else:
        return abort(500)


# @app.route('/set_food', methods=['POST'])
# def set_food_form():
#     new_food = Food(name=request.form['name'])
#
#     new_food.save()
#     return redirect('/foods')
@app.route('/api/barcode/<int:barcode>')
def get_food_from_barcode(barcode):
    food = Food.objects(barcode=barcode)
    if food:
        return food.to_json()
    else:
        #Query service to lookup product from DB
    return "Can't find item for barcode"


@app.route('/app/food/<int:id>/co2',method=['POST'])
def estimate_co2_consumption(id):
    location_data = json.load(request.data)
    food = Food.objects.get_or_404(_id=id)
    if location_data:


@app.route('/api/food/', methods=['POST'])
def set_food():
    if request.data:
        new_food_dict = json.loads(request.data)
        new_food = Food(name=new_food_dict['name'])
        for item in dir(Food):
            if item in new_food_dict:
                setattr(new_food, item, new_food_dict[item])
        new_food.save()
        if Food.objects(id=new_food.id).count() > 0:
            return "Successfully created item"
    return abort(500)


@app.route('/login', methods=["POST", "GET"])
def show_login():
    return render_template("login.html")
