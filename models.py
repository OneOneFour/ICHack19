import requests
import json
from flask_login import UserMixin
from main import mongo_db, app, login
from datetime import datetime
from edmam_wrapper import receipe_lookup
from werkzeug.security import generate_password_hash, check_password_hash
import math


class User(UserMixin, mongo_db.Document):
    username = mongo_db.StringField(required=True, unique=True)
    first_name = mongo_db.StringField(required=True)
    last_name = mongo_db.StringField(required=True)
    password = mongo_db.StringField()
    email = mongo_db.EmailField(required=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"User {self.username}"

def get_distance(a, b):
    R = 6371
    delta_lat = (a[0] - b[0]) * (math.pi / 180)
    delta_long = (a[1] - b[1]) * (math.pi / 180)
    a = math.sin(delta_lat / 2) ** 2 + math.cos(a[0]) * math.cos(b[0]) * (math.sin(delta_long / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


class Food(mongo_db.Document):
    name = mongo_db.StringField(required=True)
    barcode = mongo_db.IntField()
    country_of_origin = mongo_db.PointField()
    expiry_advice = mongo_db.StringField()
    packaging = mongo_db.FloatField()
    co2_emission_base = mongo_db.FloatField()
    FOOD_EMISSION_SITE = "https://opendata.socrata.com/resource/8nz9-yn2p.json"

    def save(self, *args, **kwargs):
        # Trawl site for info if it is available
        header = {'X-App-Token': app.config['SOCRATA_APP_TOKEN']}
        params = {'food': self.name}
        resp = requests.get(self.FOOD_EMISSION_SITE, params=params, headers=header)
        if resp.status_code == 200:
            food_data = json.loads(resp.text)
            if len(food_data) > 0:
                self.co2_emission_base = float(food_data[0]["grams_co2e_per_serving"])
        super(Food, self).save(*args, **kwargs)

    def get_recipe(self):
        return receipe_lookup(self.name)


class UserFood(mongo_db.Document):
    food = mongo_db.ReferenceField(Food, required=True, reverse_delete_rule=mongo_db.DENY)
    expiry = mongo_db.DateTimeField(required=True)
    owner = mongo_db.ReferenceField(User, required=True, reverse_delete_rule=mongo_db.CASCADE)

    def __str__(self):
        return f"{self.name} expires on {self.expiry}"

    def get_expiry_time(self):
        return (self.expiry - datetime.now()).days

    def has_expired(self):
        return (self.expiry - datetime.now()).days < 0


@login.user_loader
def load_user(id):
    return User.objects.get(id = id)
