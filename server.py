from jinja2 import StrictUndefined  

from flask import Flask, render_template, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import Artwork, Artist, ArtType, ArtTag, connect_to_db, db

# from search_form import SearchForm, connect_to_db, db

from search_form import SearchForm

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

@app.route("/form")
def form():
    form = SearchForm()

    # desriptions = db.session.query(ArtTag).filter_by(tag_code).all()
    # artists = db.session.query(Artist).filter_by(artist_name).all()
    # titles = db.session.query(Artworks).filter_by(artist_title).all()

    return render_template("search-form.html", form=form)


@app.route("/tags")
def tag_dict():

    descript = ArtTag.query.all()
    lst_tags = [r.as_dict() for r in descript]
    return jsonify(lst_tags)
    # results = Artwork.query.all()

@app.route("/process", methods=["POST"])
def process():
    tag = request.form["tag"]
    if tag:
        return jsonify({"tag": tag})
    return jsonify({"error": "missing data"})



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


