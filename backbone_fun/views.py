import re
import transaction
from sqlalchemy.exc import IntegrityError

from pyramid.response import Response
from pyramid.view import view_config

from backbone_fun.models import DBSession
from backbone_fun.models import Tweet

import json

# regular expression used to find WikiWords
wikiwords = re.compile(r"\b([A-Z]\w+[A-Z]+\w+)")

@view_config(route_name='tweet', renderer='backbone_fun:templates/post.jinja2')
def tweet(request):
    return dict(objects=get_tweets())

@view_config(route_name='tweet_api', request_method='GET', renderer='json')
def get_tweet(request):
    return dict(objects=get_tweets(),meta={})

@view_config(route_name='tweet_api', request_method='POST', renderer='json')
def post_tweet(request):
    params = request.json_body
    try:
        transaction.begin()
        session = DBSession()
        tweet = Tweet(params['username'], params['message'])
        session.add(tweet)
        transaction.commit()
    except IntegrityError:
        transaction.abort()  
    return dict(error='nope',params=params)
    
"""This really should be one line in the model.... but to convert to JSON
It seems to be requiring a little bit more massaging...  Hmmm... """
def get_tweets():
    session = DBSession()
    tweets = session.query(Tweet).all()
    list = []
    for tweet in tweets:
        list.append({
                     "id":tweet.id, 
                     "username":tweet.username, 
                     "message":tweet.message,
                     "timestamp":tweet.timestamp})
    return list
