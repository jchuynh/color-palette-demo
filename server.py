from jinja2 import StrictUndefined  

from haishoku.haishoku import Haishoku
from PIL import Image
import collections

from flask import Flask, flash, render_template, redirect, jsonify, request, url_for, session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.utils import secure_filename

from model import Artwork, Artist, ArtType, ArtTag, Tag, connect_to_db, db

import upload
import urllib.request
import requests
import json 
import os

# UPLOAD_FOLDER = "/static/user_images"
ALLOWED_EXTENSIONS = {"jpg", "jpeg"}
  

app = Flask(__name__)

app.secret_key = "whiteboardsareremarkable"

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.jinja_env.undefined = StrictUndefined


@app.route("/")
def index():
    """Displays homepage."""

    arts = Artwork.query.all()

    return render_template("index.html", arts=arts)

@app.route("/gallery")
def display_all_artworks():
    """ """
    arts = Artwork.query.all()

    return render_template("gallery.html", arts=arts)    


@app.route("/upload")
def upload_image():
    """Displays uploads page"""

    return render_template("upload.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["POST"])
def upload_submit():
    if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
    file = request.files['file']

    if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        user_img = file.save(os.path.abspath(f"static/user_images/{filename}"))

        return extract_user_palette(filename)


@app.route("/upload/user-palette")
def extract_user_palette(filename):

    def new_image(mode, size, color):
        return Image.new(mode, size, color)

    file = f"static/user_images/{filename}"

    hai = Haishoku.loadHaishoku(file)
    palette = Haishoku.getPalette(file)

    u_color_pal = []

    for item in palette:
        c_pal = item[1]
        pal = new_image('RGB', (100, 100), c_pal)
        u_color_pal.append(c_pal)

    return render_template("user-palette.html", filename=filename, 
                                                u_color_pal=u_color_pal)


### Attempting Search Function

# @app.route("/search-form", methods=["POST"])
# def search():

#     # return render_template("search-form.html")
#     search_result = request.form.get("search")

#     redirect("/search-form")


# @app.route("/search_results", methods=["POST"])
# def search_results():

#     search_result = request.forms.get("search")
#     print(search_result, "\n\n\n\n")

#     return search_result


@app.route("/search-form", methods=["POST", "GET"])
def search_items():

    # search_result = request.forms.get("search")
    # query db in background 
    # render new template w/ query results 

    user_input = request.form.get("search")

    titles = Artwork.query.filter_by(art_title).all()
    tags = Tag.query.get(tag_code).all()
    artists = Artist.query.filter(artist_name).all()
 
    all_dicts = {}

    artist_search = {"text": "artist", "children": [{"id": artist.artist_id, "text": artist.artist_name} for artist in artists]}
    tag_search = {"text": "tags", "children": [{"id": tag.tag_id, "text": tag.tag_code} for tag in tags]}
    title_search = {"text": "Artworks", "children": [{"id": artwork.artwork_id, "text": artwork.art_title} for artwork in titles]}

    results = []

    results.append(artist_search)
    results.append(tag_search)
    results.append(title_search)



    for d in results:

        all_dicts[d[text]] = [sub_d[text] for sub_d in d[children]]

        found_input = [key for key in all_dicts if user_input in all_dicts[key]][0]

        if found_input in titles:
            title = Artwork.query.filter_by(art_title=found_input).get(artwork_id)
            return render_template(f"/artworks/{title}")

        if found_input in tags:
            tag = Tag.query.filter_by(found_input).get(tag_code)
            return render_template(f"/tags/{tag}")

        if found_input in artists:
            artist = Artist.query.filter_by(found_input).get(artist_id)
            return render_template(f"/artists/{artist_id}")


        print(group_input, '\n\n\n\n\n')




@app.route("/search-test", methods=["GET", "POST"]) 
def all_query():
    """ """

    term = request.args.get("term")

    artists = Artist.query.filter(Artist.artist_name.ilike(f'%{term}%')).all()
    artist_search = {"text": "artist", "children": [{"id": artist.artist_id, "text": artist.artist_name} for artist in artists]}

    tags = ArtTag.query.filter(ArtTag.tag_code.ilike(f'%{term}%')).all()
    tag_search = {"text": "tags", "children": [{"id": tag.tag_id, "text": tag.tag_code} for tag in tags]}

    titles = Artwork.query.filter(Artwork.art_title.ilike(f'%{term}%')).all()
    title_search = {"text": "Artworks", "children": [{"id": artwork.artwork_id, "text": artwork.art_title} for artwork in titles]}

    results = []

    results.append(artist_search)
    results.append(tag_search)
    results.append(title_search)
    
    # search_results = jsonify({"results": results})
    # print({"results": results}, "\n\n\n\n")
    # return make_response(jsonify({"results": results}), 201)
    return jsonify({"results": results})



@app.route("/artworks/<int:artwork_id>")
def artwork_detail(artwork_id):
    """Displays more information on single artwork."""

    # Get the art id to display information about each piece.
    artwork = Artwork.query.get(artwork_id)

    if 'visit' not in session:
        session['visit'] = []

    if artwork.artwork_id not in session['visit']:
        session['visit'].append(artwork.artwork_id)
    session.modified = True

    # List to hold Artwork id's
    data = []

    # Get the visit dictionary out of the session or an empty one.
    visit = session.get('visit', {})

    # Loop over the visit dictionary
    for artwork_id in session['visit']:
        
        # Get the Artwork Object corresponding to this id
        site = Artwork.query.get(artwork_id)

        # Add Artwork object to list
        data.append(site)

    # When the items in the list is greater than 5, remove the first recently 
    # visited items
        if(len(data) > 5):
            data.pop(0)


    return render_template("artwork_detail.html", 
                            visit=data,
                            art_id=artwork)


@app.route("/tags/<tag_code>")
def all_tag(tag_code):
    """When tags are selected in the artwork details page"""

    tag = Tag.query.get(tag_code)

    return render_template("tag_results.html", tag=tag)


if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")


