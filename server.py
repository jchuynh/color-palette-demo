from jinja2 import StrictUndefined  

from flask import Flask, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension

from model import Artwork, Artist, ArtType, ArtTag, connect_to_db, db


import requests
import json 
  

app = Flask(__name__)

app.secret_key = "whiteboardsareremarkable"

app.jinja_env.undefined = StrictUndefined


@app.route("/")
def index():
    """Displays homepage."""

    arts = Artwork.query.all()

    return render_template("index.html", arts=arts)

### Attempting Search Function

@app.route("/search", methods["GET", "POST"])
def search():
    search = search_results()

    artists = db.session.query(Artist).filter_by(artist_name).all()
    titles = db.session.query(Artworks).filter_by(artist_title).all()
    desriptions = db.session.query(ArtTag).filter_by(tag_code).all()

    if search_results.



# @app.route("/search_results/<query>")
# def search_results():
#     results = Artwork.query.all()

#     return render_template("search_results.html", query=query)


@app.route("/artwork/<int:artwork_id>")
def artwork_detail(artwork_id):
    """Displays more information on single artwork."""

    art_id = Artwork.query.get(artwork_id)
    
    # arts = Artwork.query.all()

    return render_template("artwork_detail.html", art_id=art_id)


if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")


