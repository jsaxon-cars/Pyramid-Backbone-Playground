import re
from sqlalchemy.exc import IntegrityError

from pyramid.response import Response
from pyramid.view import view_config

from backbone_fun.models import Tweet

import json

# How to do this without the strange locator type here?
@view_config(route_name='tweet', renderer='backbone_fun:templates/post.jinja2')
def tweet(request):
  return dict(objects=Tweet.get_tweets())

@view_config(route_name='tweet_api', renderer='json')
@view_config(route_name='tweet_api_id', renderer='json')
def handle_tweet_rest(request):
  if request.method == "GET":
    if ('id' not in request.matchdict):
      return dict(objects=Tweet.get_tweets(),meta={})
    return dict(objects=Tweet.get(request.matchdict['id']),meta={})
  if request.method == "DELETE":
    tweet = Tweet.get(request.matchdict['id']) 
    Tweet.delete(tweet)
    return dict(error='nope')
  if request.method == "POST":
    tweet = Tweet(request.json_body['username'], request.json_body['message']) # DOESN'T WORK: request.param['sdfsd']
    tweet.save()  # session.add(tweet);
    return dict(error='nope')
    