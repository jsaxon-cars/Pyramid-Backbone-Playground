from backbone_fun import models
def includeme(config):
    try:
        # pyramid_alchemy
        session_factory = models.DBSession
    except AttributeError:
        # akhet
        session_factory = models.Session

    try:
        # Example for pyramid_routesalchemy and akhet
        from backbone_fun.models import MyModel
        config.formalchemy_model("/my_model", package='backbone_fun',
                                 model='backbone_fun.models.MyModel',
                                 session_factory=session_factory,
                                 view='fa.jquery.pyramid.ModelView')
    except ImportError:
        pass
    
