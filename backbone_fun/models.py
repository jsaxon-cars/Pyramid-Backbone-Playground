import transaction

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Page(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    data = Column(Text)
    #timestamp = Column(datetime)
    
    def __init__(self, name, data):
        self.name = name
        self.data = data
        #self.timestamp = now()
        
def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    #Sets up the FrontPage if none exists.
    #Handy...
    try:
        transaction.begin()
        #Why this DB session garbage in the Models file???
        session = DBSession()
        page = Page('FrontPage', 'initial data')
        #Why session.add() instead of page.save()???
        session.add(page)
        transaction.commit()
    except IntegrityError:
        # already created
        transaction.abort()