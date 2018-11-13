from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy_utils import PasswordType, force_auto_coercion
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


class User(db.Model):
    """Users of the site - users create bots only, no posts. Passwords are
    hashed using pbkdf2_sha512 via the sqlalchemy_utils package."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(PasswordType(onload=lambda **kwargs: dict(
                schemes=['pbkdf2_sha512','md5_crypt'],
                **kwargs)), unique=False, nullable=False)
    user_icon = db.Column(db.String(255), nullable=False)
    user_description = db.Column(db.String(255), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)


    def __repr__(self):
        """Provides basic user info when printed."""

        return f"<User ID={self.user_id}, Username={self.username}>"


class Bot(db.Model):
    """Bots created via user data."""

    __tablename__ = "bots"

    bot_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    source_id = db.Column(db.Integer, db.ForeignKey('sources.source_id'), nullable=False)
    bot_name = db.Column(db.String(64), nullable=False)
    bot_icon = db.Column(db.String(255), nullable=False)
    bot_description = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

    user = db.relationship("User", backref=db.backref('bots',
                                                      order_by=bot_id))

    posts = db.relationship("Post", backref=db.backref('bot',
                                                      order_by=bot_id))

    source = db.relationship("Source", backref=db.backref('bot',
                                                      order_by=bot_id))

    def __repr__(self):
        """Provides basic bot info when printed."""

        return f"<Bot ID={self.bot_id}, Name={self.bot_name}>"


class Source(db.Model):
    """Contains content used for post generation. These sources are stored
    as follows:
    source_id = autoincrementing index for rows
    content_type = might be helpful in the future, but for now, most are 'twitter'
    content_source = content identifier (twitter handle, NLTK corpus, etc)
    content = one large string of text. used for generating markov chains,
              chains can be generated from multiple sources via concatenation"""

    __tablename__ = "sources"

    source_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    content_type = db.Column(db.String(30))
    content_source = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        """Provides content info when printed."""

        return f"<Source ID={self.source_id}, type={self.content_type}, \n sample={self.content[:30]}...>"


class Post(db.Model):
    """Contains content created by bots."""

    __tablename__ = "posts"

    post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    bot_id = db.Column(db.Integer, db.ForeignKey('bots.bot_id'))
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

    def __repr__(self):
        """Provide simple post info when printed."""

        return f"<{self.content}>"


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
