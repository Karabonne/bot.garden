from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import time
from datetime import date, datetime

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

##############################################################################
# Model definitions

def connect_to_db(app):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///testdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


class Bot(db.Model):
    """Bots created via user data."""

    __tablename__ = "bots"

    bot_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    source = db.Column(db.Text, nullable=False)
    bot_name = db.Column(db.String(64), nullable=False)
    bot_icon = db.Column(db.String(255), nullable=False)
    bot_description = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

    user = db.relationship("User", backref=db.backref('bot',
                                                      order_by=bot_id))

    post = db.relationship("Post", backref=db.backref('bot',
                                                      order_by=bot_id))

    def __repr__(self):
        """Provides basic bot info when printed."""

        return f"<Bot ID={self.bot_id}, Name={self.bot_name}>"


class User(db.Model):
    """Users of the site - users create bots only, no posts."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_icon = db.Column(db.String(255), nullable=False)
    user_description = db.Column(db.String(255), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        """Provide basic user info when printed."""

        return f"<User ID={self.user_id}, Email={self.email}>"


class Post(db.Model):
    """Contains content created by bots."""

    __tablename__ = "posts"

    post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    bot_id = db.Column(db.Integer, db.ForeignKey('bots.bot_id'))
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        """Provide simple post info when printed."""

        return f"<Post ID={self.post_id}, Bot ID={self.bot_id}>"


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
