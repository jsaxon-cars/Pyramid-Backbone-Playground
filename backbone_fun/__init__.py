from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.response import Response

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
    #config.add_route('home', '/')
    #config.add_route('post','post')
    
    config.add_route('post', 'post/{id:[^/\.]+}')
    
    config.add_route('view_wiki','/')
    config.add_route('view_pages', 'page/')
    config.add_route('view_page', 'page/{pagename}')
    config.add_route('add_page', 'page/add_page/{pagename}')
    config.add_route('edit_page', 'page/{pagename}/edit_page')

    config.add_view('backbone_fun.views.view_wiki', 
                    route_name='view_wiki')
    config.add_view('backbone_fun.views.view_pages', 
                    route_name='view_pages',
                    renderer='backbone_fun:templates/view.jinja2')
    config.add_view('backbone_fun.views.view_page', 
                    route_name='view_page',
                    renderer='backbone_fun:templates/view.jinja2')
    config.add_view('backbone_fun.views.add_page', 
                    route_name='add_page',
                    renderer='backbone_fun:templates/edit.jinja2')
    config.add_view('backbone_fun.views.edit_page', 
                    route_name='edit_page',
                    renderer='backbone_fun:templates/edit.jinja2')
 
    config.scan('backbone_fun')
    return config.make_wsgi_app()

