from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager


# Create flask app
app = Flask(__name__)

# Connect to DB
app.config["MONGODB_SETTINGS"] = {
    'db': 'foods',
    'host': 'localhost',
    'port': 27017
}
app.config['EDAMAM_APP_ID'] = "6fc94a08"
app.config["EDAMAM_APP_AUTH"] = "015f0b82bfdad03e657f4cecf3b0586d"

app.config["SOCRATA_APP_TOKEN"] = "fw89kSX55yjwub5zQ1FRNaOuW"
app.config["SOCRATA_SECRET_TOKEN"] = "NsMtdhERY1MT-AFJEl_zWGnCWwaCxr86zN_a"

app.config['SECRET_KEY'] = 'secretlog' #for github logins


mongo_db = MongoEngine()
mongo_db.init_app(app)

# Creating login instance
login = LoginManager(app)

DEBUG = True

# We import views after setting things up but BEFORE app.run to ensure the functions for the views have all been defined in time
from .views import *

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=DEBUG)


