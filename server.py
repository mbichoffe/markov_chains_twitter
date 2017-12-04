
from flask import Flask, render_template, request, flash, redirect, session, \
    jsonify
from flask_debugtoolbar import DebugToolbarExtension
from markov import *
import requests
from jinja2 import StrictUndefined
import json
# import calendar
app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "AIRSPEEDVELOCITYOFANUNLADENSWALLOW"


@app.route('/')
def index():
    
    """Main page."""


app.jinja_env.undefined = StrictUndefined
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = False

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(debug=True, host="0.0.0.0", port=5000)