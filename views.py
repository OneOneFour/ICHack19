import json
import re
import requests
from flask_login import current_user, login_user, logout_user
from flask import render_template, request, redirect, abort, jsonify, url_for, flash
from main import app, mongo_db
from models import Food, User


# #from flask_dance.contrib.github import make_github_blueprint, github
#
# #github_blueprint = make_github_blueprint(client_id='b7fe8aa6299d7d8aa187',
#                                          client_secret='935f2cf040042bdea0a5f70d525e21bcc8b92b6a')
#
# app.register_blueprint(github_blueprint, url_prefix='/github_login')


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", current_user=current_user)

@app.route('/aboutUs')
def aboutUs():
    return render_template("aboutUs.html")


@app.route('/foods')
def show_foods():
    foods = Food.objects
    return render_template("ideal.html", foods=foods)


@app.route('/api/delete_food/<id>')
def delete_food(id):
    Food.objects.get_or_404(_id=id)
    if Food.objects(_id=id).count() == 0:
        return "Item deleted successfully"
    else:
        return f"Error deleting item with id:{id}"


@app.route('/search_food/', methods=['GET'])
def search_food():
    q = request.args.get("search_food")
    f, recipes = None, None
    if q:
        f = Food.objects(name__icontains=q).first()
        f.save()
    return render_template("ideal.html", foods=[f,])


@app.route('/recipes/<id>')
def recipes(id):
    food = Food.objects.get_or_404(id=id)
    if food:
        recipes = food.get_recipes()
        return render_template("recipes.html", recipes=recipes)
    return abort(400)


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
        return jsonify(food.get_recipes())
    else:
        return abort(404)


@app.route("/api/food/remove/", methods=["POST"])
def remove_food_from_db():
    delete_food_dict = json.loads(request.data)
    food = Food.objects.get_or_404(_id=delete_food_dict["id"])
    food.delete()
    if Food.objects(_id=delete_food_dict["id"]).count() == 0:
        return jsonify({'result': 1})
    else:
        return abort(500)


@app.route("/api/food/<int:id>", methods=['PUT'])
def update_food(id):
    food = Food.objects.get_or_404(_id=id)
    if request.data:
        data_to_update = json.loads(request.data)
        for (key, value) in data_to_update.iteritems():
            setattr(food, key, value)
        return food.to_json()
    return abort(500)


@app.route('/api/barcode/<int:barcode>')
def get_food_from_barcode(barcode):
    food = Food.objects(barcode=barcode)
    if food:
        return food.to_json()
    else:
        resp = requests.get(f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json")
        if resp.status_code == 200:
            resp_dict = json.loads(resp.text)
            if resp_dict['status'] == 1:
                food_data = resp_dict['product']
                # Has found a barcode in the openfoodfacts db
                food = Food(name=food_data["product_name"], barcode=barcode)
                food.save()
                return food.to_json()
    return "Can't find item for barcode"


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
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = User.objects(username=request.form['username']).first()
        if user is None or not user.check_password(request.form['password']):
            flash("Your username or password is not valid. Please check your details and try again")
            return redirect('login')
        remember_me = bool(request.form['remember_me'])
        login_user(user, remember_me)
        return redirect(url_for('index'))
    return render_template("login.html", title="Login")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == 'POST':
        if User.objects(username=request.form["username"]).count() > 0:
            flash("THIS USERNAME ALREADY EXISTS")
            return redirect("signup")
        if request.form['password'] != request.form['confirm_password']:
            flash("Passwords must match")
            return redirect("signup")
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", request.form["email"]):
            flash("Email is not valid. Please enter a valid email")
            return redirect("signup")
        new_user = User(username=request.form["username"], email=request.form['email'],
                        first_name=request.form['first_name'], last_name=request.form['last_name'])
        new_user.set_password(request.form['password'])
        new_user.save()
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template("signup.html", title="Signup")


# @app.route('/github')
# def github_login():
#     if not github.authorized:
#         return redirect(url_for('github.login'))
#
#     account_info = github.get('/user')
#
#     if account_info.ok:
#         # account_info_json = account_info.json()
#
#         # return '<h1>Your Github name is {}'.format(account_info_json['login'])
#         return redirect(url_for('index'))
#
#     return '<h1>Request failed!</h1>'


@app.route('/logout')
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    logout_user()
    if current_user.is_authenticated:
        flash("Unable to log user out. Please try again")
    else:
        flash("You have been logged out, have a nice day!")
    return redirect(url_for('index'))


@app.route('/recover')
def recover():
    return render_template("forgot.html")
