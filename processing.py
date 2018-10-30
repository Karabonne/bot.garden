import markov
from twitter import *
from config import *


# Initialize our twitter session
t = Twitter(
    auth=OAuth(access_token, token_secret, api_key, api_secret))


def get_tweets(username):
    """
    Get tweets from a user, strip out all data except text, then
    create a list of tweet text. """

    #grabs a set of user tweets
    tweets = t.statuses.user_timeline(screen_name=username,
                                          include_rts="false",
                                          exclude_replies="true")

    text_list = [item['text'] for item in tweets]

    return text_list
