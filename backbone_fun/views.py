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

@view_config(route_name='tweet_api', request_method='GET', renderer='json')
def get_tweet(request):
    return dict(objects=Tweet.get_tweets(),meta={})

@view_config(route_name='tweet_api', request_method='POST', renderer='json')
def post_tweet(request):
    tweet = Tweet(request.json_body['username'], request.json_body['message']) # DOESN'T WORK: request.param['sdfsd']
    tweet.save()  # session.add(tweet);
    return dict(error='nope')
    