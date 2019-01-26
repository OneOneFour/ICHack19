import requests
from . import app
import json

def receipe_lookup(query):
    params = {"app_id": app.config['EDAMAM_APP_ID'], "app_key": app.config['EDAMAM_APP_AUTH'], "q": query}
    r = requests.get("https://api.edamam.com/search", params)
    print(r.url)
    if r.status_code == 200:
        return json.loads(r.text)["hits"]
    else:
        raise Exception("Unable to contact api")
