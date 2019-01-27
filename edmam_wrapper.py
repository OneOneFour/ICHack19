import requests
from main import app
import json

intresting_keys = ("label","image", "url", "calories", "healthLabels")


def receipe_lookup(query):
    params = {"app_id": app.config['EDAMAM_APP_ID'], "app_key": app.config['EDAMAM_APP_AUTH'], "q": query,"to":5}
    r = requests.get("https://api.edamam.com/search", params)
    if r.status_code == 200:
        return [{k: hit["recipe"][k] for k in intresting_keys} for hit in json.loads(r.text)["hits"]]
    else:
        raise Exception("Unable to contact api")
