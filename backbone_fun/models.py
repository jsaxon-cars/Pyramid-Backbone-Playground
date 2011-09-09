import transaction
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import DateTime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Tweet(Base):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True)
    username = Column(Text)
    message = Column(Text)
    timestamp = Column(DateTime)
    
    def __init__(self, username, message):
        self.username = username
        self.message = message
        self.timestamp = datetime.now()

    @staticmethod
    def get_tweets():
        session = DBSession()
        tweets = session.query(Tweet).all()
        list = []
        for tweet in tweets:
            list.append({
                         "id":tweet.id, 
                         "username":tweet.username, 
                         "message":tweet.message,
                         "timestamp":tweet.timestamp.strftime('%x %X')})
        return list
        
def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    
    #This wipes out the database every time...
    Base.metadata.drop_all(engine) 
    
    Base.metadata.create_all(engine)
    try:
        session = DBSession()
        tweet = Tweet('Fred', 'Yet another tweet for fun')
        #Why session.add() instead of page.save()???
        session.add(tweet)
        transaction.commit()
    except IntegrityError:
        # already created
        pass