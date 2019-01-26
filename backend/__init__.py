from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
#Create flask app
app = Flask(__name__)

#Connect to DB
app.config["MONGO_URI"] = "mongodb://localhost:27017/foods"
mongo_db = PyMongo(app)

#Creating login instance
login = LoginManager(app)

DEBUG = True

#We import views after setting things up but BEFORE app.run to ensure the functions for the views have all been defined in time
from .views import *

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=DEBUG)
