"""Flask app for Cupcakes"""

from flask import Flask, flash, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


def serialize_cupcake(cupcake):
    """Serializing cupcake."""

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }


@app.route("/api/cupcakes")
def get_cupcakes():
    """Get all cupcakes.
    Should return JSON {cupcakes: [{id, flavor, size, rating, image}, ...]}."""

    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Get all a cupcake.
    Should return JSON {cupcake: {id, flavor, size, rating, image}}."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Create a new cupcake.
    Should return JSON {cupcake: {id, flavor, size, rating, image}}."""

    new_cupcake = Cupcake()

    new_cupcake.flavor = request.json["flavor"]
    new_cupcake.size = request.json["size"]
    new_cupcake.rating = request.json["rating"]
    new_cupcake.image = request.json["image"]

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)

    return (jsonify(cupcake=serialized), 201)
