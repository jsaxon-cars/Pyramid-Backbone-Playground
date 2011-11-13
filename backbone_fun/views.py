import re
from sqlalchemy.exc import IntegrityError

from pyramid.response import Response
from pyramid.view import view_config

from backbone_fun.models import Tweet

import json

# regular expression used to find WikiWords
wikiwords = re.compile(r"\b([A-Z]\w+[A-Z]+\w+)")

@view_config(route_name='tweet', renderer='backbone_fun:templates/post.jinja2')
def tweet(request):
	#print Tweet.get_tweets()
    return dict(objects=Tweet.get_tweets())

@view_config(route_name='tweet_api', request_method='GET', renderer='json')
def get_tweet(request):
    return dict(objects=Tweet.get_tweets(),meta={})

@view_config(route_name='tweet_api', request_method='POST', renderer='json')
def post_tweet(request):
    tweet = Tweet(request.json_body['username'], request.json_body['message'])
    tweet.save()
    # THIS SHOULD BE A REDIRECT???  No, that would be for backarrow post issues!
    #HTTPFound('/tweet')
    return dict(error='nope')
    