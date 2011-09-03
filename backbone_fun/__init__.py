from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from backbone_fun.models import initialize_sql

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    config = Configurator(settings=settings)
    config.add_static_view('static', 'backbone_fun:static')
    config.add_route('home', '/')
    config.add_view('backbone_fun.views.my_view',
                    route_name='home',
                    renderer='templates/mytemplate.pt')
    return config.make_wsgi_app()

