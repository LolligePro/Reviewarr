from sqlalchemy import create_engine, Integer, String, Float, Date, Column, ForeignKey, CheckConstraint
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///./reviewarr.db', echo=True)
Base = declarative_base()

class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    rating = Column(Float)
    reviewer_id = Column(Integer, ForeignKey('users.id'))
    media_id = Column(Integer, ForeignKey('media.id'))

    __table_args__ = (CheckConstraint('rating >= 0 AND rating <= 1'),)

    def __string__(self):
        return 'media_id: ' + str(self.media_id) + ', title: ' + self.title + ', rating: ' + str(self.rating) + ', reviewer_id: ' + str(self.reviewer_id)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)

    def __string__(self):
        return  'id: ' + str(self.id) + ', username: ' + str(self.username)

def init_db():
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()