from jinja2 import StrictUndefined  

from flask import Flask, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension

from model import Artwork, Artist, ArtType, connect_to_db, db

import requests
import json 
  

app = Flask(__name__)

app.secret_key = "whiteboardsareremarkable"

url = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
response = requests.get(url)
data = response.json() 

for item in data:
    new_url = 

##### API #####

# url = "https://collectionapi.metmuseum.org/public/collection/v1/objects/436530"
# response = requests.get(url)
# data = response.json()

# objects = json.dumps(data)


# def get_data():

#     art_info = []

#     for item in objects:
#         art_info_dict = {}

#         art_info_dict['art_title'] = data.get('title')
#         art_info_dict['artist_name'] = data.get('artistDisplayName') 
#         art_info_dict['art_image'] = data.get('primaryImageSmall')
#         art_info_dict['type_code'] = data.get('classification')
#         art_info.append(art_info_dict)
#     return art_info









# payload = {'title': art_title,
#            'artistDisplayName': artist_name,
#            'classification': art_media_code,
#            'primaryImageSmall': art_image}


ß
@app.route("/")
def index():
    """Displays homepage."""

    art_image = request.args.get("art_image")

    return render_template("../templates/index.html", art_image=art_image)

# @app.route("/artwork/{artwork_id}")
# def artwork_detail(artwork_id):
#     """Displays more information on single artwork."""

#     artwork_id = Artwork.query.get(artwork_id)
#     art_title = Artwork.query.get(art_title)
#     art_image = Artwork.query.get(art_image)

#     return render_template("artwork.html", artwork_id=artwork_id)


if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")


