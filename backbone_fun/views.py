import re
import transaction
from sqlalchemy.exc import IntegrityError

from docutils.core import publish_parts
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.url import route_url

from pyramid.response import Response
from pyramid.view import view_config

from backbone_fun.models import DBSession
from backbone_fun.models import Tweet

import json

# regular expression used to find WikiWords
wikiwords = re.compile(r"\b([A-Z]\w+[A-Z]+\w+)")

@view_config(route_name='post', request_method='GET', renderer='json')
def posts(request):
    return dict(pages="nothing",meta={})

@view_config(route_name='post', request_method='DELETE', renderer='json')
def delete_post_view(request):
    return request.matchdict

@view_config(route_name='tweet', renderer='backbone_fun:templates/post.jinja2')
def tweet(request):
    return dict(objects=get_tweets())

@view_config(route_name='tweet_api', request_method='GET', renderer='json')
def get_tweet(request):
    return dict(objects=get_tweets(),meta={})

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

@view_config(route_name='tweet_api', request_method='POST', renderer='json')
def post_tweet(request):
    params = request.json_body
    try:
        transaction.begin()
        session = DBSession()
        print "ADDING A TWEET NOW =================="
        tweet = Tweet(params['username'], params['message'])
        print "ADDING A TWEET NOW =================="
        print tweet
        session.add(tweet)
        transaction.commit()
    except IntegrityError:
        # already created
        transaction.abort()  
    return dict(error='nope',params=params)
    
