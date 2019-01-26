from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/foods"
mongo_db = PyMongo(app)

DEBUG = True

from .views import *

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=DEBUG)
