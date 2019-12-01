from flask import Flask, render_template, request, redirect, url_for, flash, \
    Response
from flask_sqlalchemy import SQLAlchemy
from formencode import Schema, Invalid
from formencode.validators import Number, Bool, ByteString

# Create the Flask app
app = Flask(__name__)

# Define the connection to the database. For simplicity's sake,
# we'll use an in-memory SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

# Track modifications is deprecated. Turning it off gets rid of a warning.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# This is a properly random 32 bit secret key generated via:
#        "".join([chr(secrets.randbits(8)) for x in range(32)]).encode()
app.secret_key = b"\xc3\xb8\xc3\x8ei\xc3\xa7d\xc2\xa0@\xc3\xb8\x15\xc3\xbd" \
                 b"\xc2\x9d\xc3\xb5\xc2\x86L^0}\x12,\\\x01\xc2\xa8P\xc3\xb2" \
                 b"\xc2\xber@\xc3\xaf\x02(\xc2\xa8\t"

# Initialize Flask SQLAlchemy
db = SQLAlchemy(app)


# Define the model
class ToDoItem(db.Model):
    """
    This is the SQL Alchemy model for out application. It will be used to
    create the table when the application starts an manage the data
    once it's up and running.

    :id: The unique identifier for the item
    :description: The description of the item
    :completed: has the item been completed
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    description = db.Column(db.String(50), nullable=False)
    completed = db.Column(db.Boolean, default=False)


# Create the database schema from the models. This is done to simplify the
# example and would never be used in a production app.
db.create_all()


# Define request validators. These validators will be used to take request
# form data and return a validated and transformed dictionary that is safe and
# ready to use
class PostValidator(Schema):
    """
    Validator for the post action
    """
    description = ByteString(max=50, not_empty=True)


class PatchValidator(Schema):
    """
    Validator for the patch action
    """
    id = Number
    completed = Bool


class DeleteValidator(Schema):
    """
    Validator for the delete action
    """
    id = Number


# Define the routes
@app.route("/", methods=["GET"])
def index() -> Response:
    """
    Handler for GET requests to the / path.
    """

    # Get all the items
    items = ToDoItem.query.all()

    # Send the items to the index.html template to be rendered
    return render_template("index.html", items=items)


@app.route("/post", methods=['POST'])
def post() -> Response:
    """
    Handler for POST requests to the /post path. This will create an new item
    """
    try:
        # Validate and transform the POST data with the validator
        form_data = PostValidator().to_python(request.form)
        # Create a new item with the description from the request
        item = ToDoItem(description=form_data['description'])
        # Add the item
        db.session.add(item)
        # Save the changes to the database
        db.session.commit()
    except Invalid as e:
        # If there is an error in the POST data, flash an error message
        flash(e.msg, "error")

    # Redirect to the index to show the result
    return redirect(url_for('index'))


@app.route("/patch", methods=['POST'])
def patch() -> Response:
    """
    Handler for POST requests to the /post path. This will update an existing
    item
    """
    try:
        # Validate and transform the POST data with the validator
        form_data = PatchValidator().to_python(request.form)
        # Get the item to update by its ID
        item = ToDoItem.query.get(form_data['id'])
        # Update the completed field based on the date from request
        item.completed = form_data['completed']
        # Save the changes to the database
        db.session.commit()
    except Invalid as e:
        # If there is an error in the POST data, flash an error message
        flash(e.msg, "error")

    # Redirect to the index to show the result
    return redirect(url_for('index'))


@app.route("/delete", methods=['POST'])
def delete():
    """
    Handler for POST requests to the /post path. This will delete an existing
    item
    """
    try:
        # Validate and transform the POST data with the validator
        form_data = DeleteValidator().to_python(request.form)
        # Get the item by its ID
        item = ToDoItem.query.get(form_data['id'])
        # Delete the item
        db.session.delete(item)
        # Save the changes to the database
        db.session.commit()
    except Invalid as e:
        # If there is an error in the POST data, flash an error message
        flash(e.msg)

    # Redirect to the index to show the result
    return redirect(url_for('index'))


# Define the lifecycle events
@app.before_first_request
def before_first_request():
    """
    This function is registered to run before the first request. There are
    a number of other lifecycle events that can be registered.

    This will show the first request after starting that we are starting fresh
    """
    flash("Starting fresh")
