import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Error(Exception):
	pass

class AlreadyInDB(Error):
	pass

class Album(Base):
	__tablename__ = "album"
	id = sa.Column(sa.INTEGER, primary_key=True)
	year = sa.Column(sa.INTEGER)
	artist = sa.Column(sa.TEXT)
	genre = sa.Column(sa.TEXT)
	album = sa.Column(sa.TEXT)

def connect_db():
	engine = sa.create_engine(DB_PATH)
	Base.metadata.create_all(engine)
	session = sessionmaker(engine)
	return session()

def find(artist):
	session = connect_db()
	albums = session.query(Album).filter(Album.artist == artist).all()
	return albums

def save_new_album(year, artist, genre, album):
	session = connect_db()
	saved_album = session.query(Album).filter(Album.artist == artist, Album.album == album).first()

	if saved_album is not None:
		raise AlreadyInDB("The album already exists in the database by the id {}".format(saved_album.id))
	else:
		album = Album(year=year, artist=artist, genre=genre, album=album)
		session.add(album)
		session.commit()
	return album	