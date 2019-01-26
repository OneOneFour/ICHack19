from . import mongo_db,app
from datetime import datetime
from .edmam_wrapper import receipe_lookup

class Food(mongo_db.Document):
    name = mongo_db.StringField(required=True)
    expiry = mongo_db.DateTimeField()

    def __str__(self):
        return f"{self.name} expires on {self.expiry}"

    def get_expiry_time(self):
        return (self.expiry - datetime.now()).days

    def has_expired(self):
        return (self.expiry - datetime.now()).days < 0

    def get_recipe(self):
        return str(receipe_lookup(self.name))


