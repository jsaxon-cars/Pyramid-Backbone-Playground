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
    config.include('pyramid_formalchemy')

    # register an admin UI
    config.formalchemy_admin('admin', package='backbone_fun')

    # register an admin UI for a single model
    config.formalchemy_model('tweety', package='backbone_fun', model='backbone_fun.models.Tweet')

    # register custom model listing
    config.formalchemy_model_view('admin',
                                  model='backbone_fun.models.Tweet',
                                  context='pyramid_formalchemy.resources.ModelListing',
                                  #renderer='templates/tweetlisting.jinja2',
                                  attr='listing',
                                  request_method='GET',
                                  permission='view')

    # register custom model view
    config.formalchemy_model_view('admin',
                                  model='backbone_fun.models.Tweet',
                                  context='pyramid_formalchemy.resources.Model',
                                  name='',
                                  #renderer='templates/tweetshow.jinja2',
                                  attr='show',
                                  request_method='GET',
                                  permission='view')


    config.add_static_view('static', 'backbone_fun:static')
    config.add_route('tweet','tweet')   
    config.add_route('tweet_api','tweet/api/')   
    
    #tweens
    '''
    config.add_tween(
      'useless.useless_tween_factory', 
      over=pyramid.tweens.MAIN,
      under='useless.useless_tween_factory')
    '''
 
    config.scan('backbone_fun')

    return config.make_wsgi_app()

