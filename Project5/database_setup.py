import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    access_token = Column(String(200))

    def __init__(self, access_token):
        self.access_token = access_token

class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)

    @property
    def serialize(self):
        """ JSON serializer method """
        return {
            'id': self.id,
            'name': self.name,
        }

class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    song_url = Column(String(255))
    description = Column(String(1000))
    featured = Column(Boolean, default=False)
    artist_id = Column(Integer, ForeignKey('artists.id'))
    artist = relationship(Artist)
    adder_id = Column(Integer, ForeignKey('users.id'))
    adder = relationship(User)

    @property
    def serialize(self):
        """ JSON serializer method """
        return {
            'id': self.id,
            'name': self.name,
            'song_url': self.song_url,
            'description': self.description,
            'featured': self.featured,
            'artist_id': self.artist_id
        }

engine = create_engine('postgresql://flask:valarmorghulis@localhost/udacity_song')
Base.metadata.create_all(engine)
