"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request, render_template
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


@app.route('/')
def index():
    """ Display form to add cupcakes. """

    return render_template('index.html')


@app.route("/api/cupcakes")
def get_cupcakes():
    """Get all cupcakes.
    Should return JSON {cupcakes: [{id, flavor, size, rating, image}, ...]}."""

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)


@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Get all a cupcake.
    Should return JSON {cupcake: {id, flavor, size, rating, image}}."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Create a new cupcake.
    Should return JSON {cupcake: {id, flavor, size, rating, image}}."""

    new_cupcake = Cupcake()

    new_cupcake.flavor = request.json["flavor"]
    new_cupcake.size = request.json["size"]
    new_cupcake.rating = request.json["rating"]
    new_cupcake.image = request.json.get("image") or None

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update an existing cupcake.
    Should return JSON {cupcake: {id, flavor, size, rating, image}}."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json["flavor"]
    cupcake.size = request.json["size"]
    cupcake.rating = request.json["rating"]
    cupcake.image = request.json["image"]

    db.session.add(cupcake)
    db.session.commit()

    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete an existing cupcake.
       Should return JSON {message: "Deleted"}."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")
