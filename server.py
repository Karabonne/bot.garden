"""server file for bot playground."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from datetime import date, datetime
from model import Bot, User, Post, connect_to_db, db

import json

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC123456hackbright"

# catches Jinja2 erorrs
app.jinja_env.undefined = StrictUndefined

# 1. INFO DISPLAY SECTION ---------------------------------

@app.route('/')
def show_index():
    """TODO: Main page - shows a stream of bot posts."""

    return render_template("homepage.html")


@app.route('/user/<user_id>')
def show_user_page(user_id):
    """TODO: Shows a user info page, including list of user's bots."""

    user = User.query.get(user_id)
    user_bots = Bot.query.filter_by(user_id=user_id).all()

    return render_template("user.html",
                              user=user,
                              user_bots=user_bots)


@app.route('/bot/<bot_id>')
def show_bot_page(bot_id):
    """TODO: Shows a bot info page, including posts and creator."""

    bot = Bot.query.get(bot_id)
    creator = Bot.query.filter_by(user_id)
    bot_posts = Post.query.filter_by(bot_id=bot_id).all()

    pass


@app.route('/')
def show_bot_directory():
    """Shows a bot directory."""

    bot_entries = Bot.query.all()

    return render_template("bots.html", bots=bot_entries)

# 2. USER REGISTRATION AND LOGIN SECTION ------------------

@app.route("/register", methods=["GET"])
def show_reg_form():
    """Displays a user registration form."""

    return render_template("registration.html")


@app.route("/register", methods=["POST"])
def process_reg():
    """Adds user to DB."""

    new_email = request.form.get('email')
    pswd = request.form.get('password')
    desc = request.form.get('description')

    # Check for user email in db
    db_email = User.query.filter(User.email == new_email).first()

    if not db_email:
        user = User(email=new_email,
                 password=pswd,
                 user_icon="icon001",
                 user_description=desc,
                 date_created=datetime.today())
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
    else:
        flash('Email address already exists - try again?')

    return redirect("/")


@app.route("/login", methods=["POST"])
def login_user():
    """Adds user information to session."""

    login_email = request.form.get('email')
    pswd = request.form.get('password')

    user = User.query.filter(User.email == login_email).first()


    if user:
        if user.password == pswd:
            # add user info to Flask session
            session['user_id'] = user.user_id
            session['email'] = user.email
            flash('Successfully logged in!')
            return redirect("/")
        else:
            flash('Invalid password!')
    else:
        flash('User not found!')

    return redirect("/")


@app.route("/logout")
def log_out():
    """Logs user out of session."""

    session.clear()

    return redirect("/")

# 3. BOT CREATION AND LOGIC SECTION -----------------------

@app.route("/create", methods=["GET"])
def show_bot_form():
    """Displays a bot creation form."""

    return render_template("create.html")


@app.route("/create", methods=["POST"])
def create_bot():
    """Adds bot to DB."""

    name = request.form.get('email')
    desc = request.form.get('description')
    data_source = request.form.get('twitter')

    bot = Bot(bot_name=bot_name,
                 bot_description=desc,
                 bot_icon='icon001',
                 source=data_source,
                 date_created=datetime.today())
    db.session.add(user)
    db.session.commit()
    
    flash('It lives....it lives!')
    

    return redirect("/")

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
