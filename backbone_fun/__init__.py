from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid.view import view_config

from backbone_fun.models import initialize_sql

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    config = Configurator(settings=settings)
    
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'backbone_fun:static')
    config.add_route('tweet','tweet')   
    config.add_route('tweet_api','tweet/api/{id}')   
 
    config.scan('backbone_fun')

    return config.make_wsgi_app()

