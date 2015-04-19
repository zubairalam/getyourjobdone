from __future__ import unicode_literals
import json
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs

from constance import config


REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
AUTHORIZE_URL = 'https://api.twitter.com/oauth/authorize?oauth_token='
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'

CONSUMER_KEY = config.SOCIAL_TWITTER_CONSUMER_KEY
CONSUMER_SECRET = config.SOCIAL_TWITTER_CONSUMER_SECRET
OAUTH_TOKEN = config.SOCIAL_TWITTER_OAUTH_TOKEN
OAUTH_TOKEN_SECRET = config.SOCIAL_TWITTER_OAUTH_SECRET


def setup_oauth():
    """
    Authorize your app via identifier.
    """
    # Request token
    oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)

    resource_owner_key = credentials.get('oauth_token')[0]
    resource_owner_secret = credentials.get('oauth_token_secret')[0]

    # Authorize
    authorize_url = AUTHORIZE_URL + resource_owner_key
    print('Please go here and authorize: ' + authorize_url)

    verifier = raw_input('Please input the verifier: ')
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
                   verifier=verifier)

    # Finally, Obtain the Access Token
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    token = credentials.get('oauth_token')[0]
    secret = credentials.get('oauth_token_secret')[0]

    return token, secret


def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=OAUTH_TOKEN,
                   resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth


def get_tweets(twitter_name, tweet_count):
    try:
        if OAUTH_TOKEN:
            tweets = []
            oauth = get_oauth()
            url_format = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=%s&count=%s' % (
                twitter_name, tweet_count)
            r = requests.get(url=url_format, auth=oauth)
            for x in r.json():
                tweets.append(json.dumps(x['text']))
            return tweets

    except ValueError:
        return []


