import flask
from sqlalchemy import func
from sqlalchemy_utils import PasswordType, force_auto_coercion
import markovify
import nltk
from server import app
from model import Bot, User, Post, Source, connect_to_db, db
from processing import *

connect_to_db(app)

def add_users():
    """Add users from a seed file. Data is stored in this format:

    username|password|user_icon|user_description
    """

    print("Users")

    # Deletes any existing data in the users table
    User.query.delete()

    for line in open("seed_files/users.txt"):
        line = line.rstrip()
        username, password, user_icon, user_description = line.split("|")

        user = User(username=username,
                      password=password,
                      user_icon=user_icon,
                      user_description=user_description)

        db.session.add(user)

    db.session.commit()


def add_sources():
    """Add sources to the database. Sources are built as follows:

    1. read from input file, contains the following:
        content_type|content_source
    2. for twitter sources:
            grab username from 'content_source', retrieve all tweets, collate
            the text into one large string
        for nltk sources:
            retrieve corpus name from 'content_source', download from
            nltk database if required, and use nltk functions to store corpus
            as one large text file
    3. add above to database
    """

    print("Sources")

    # Deletes any existing data in the users table
    Source.query.delete()


    for line in open("seed_files/sources.txt"):
        line = line.rstrip()
        content_type, content_source = line.split("|")

        if content_type == "twitter":

            content = ' '.join(get_tweets(content_source))

        elif content_type == "nltk":

            nltk.download(content_source)
            text = getattr(nltk.corpus, content_source)
            content =  ' '.join(text.words())

        else:

            print("Invalid source! Aborting...")
            break

        source = Source(content_type=content_type,
                               content_source=content_source,
                               content=content)

        db.session.add(source)

    db.session.commit()


def add_bots():
    """Add bots from a seed file. Data is stored in this format:

    creator_id|content_id|bot_name|bot_icon|bot_description
    """

    print("Bots")

    # Deletes any existing data in the bots table
    Bot.query.delete()

    for line in open("seed_files/bots.txt"):
        line = line.rstrip()

        creator_id, source_id, bot_name, bot_icon, bot_description = line.split("|")

        bot = Bot(creator_id=creator_id,
                      source_id=source_id,
                      bot_name=bot_name,
                      bot_icon=bot_icon,
                      bot_description=bot_description)

        db.session.add(bot)

    db.session.commit()

def add_posts():
    """Generate a number of sample posts."""
    
    pass

if __name__ == "__main__":

    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # add_users()
    # add_bots()
    # add_sources()
