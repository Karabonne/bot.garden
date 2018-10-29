"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import Bot, User, Post, connect_to_db, db

import json

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC123456hackbright"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def show_index():
    """Main page - shows a stream of bot posts."""

    bot_entries = Bot.query.all()

    return render_template("homepage.html", bots=bot_entries)


@app.route('/user/<user_id>')
def show_user_page():
    """TODO: Shows a user info page, including list of user's bots."""


    pass


@app.route('/bot/<bot_id>')
def show_bot_page():
    """TODO: Shows a bot info page, including posts and creator."""


    pass

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
