from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album

@route("/albums/<artist>")
def albums(artist):
	albums_list = album.find(artist)
	if not albums_list:
		message = "No albums of the artist {} have been found".format(artist)
		result = HTTPError(400, message)
	else:
		album_names = [album.album for album in albums_list]
		result = "The artist {} has {} albums: <br>".format(artist, len(albums_list))
		result += "<br>".join(album_names)
	return result

@route("/albums", method="POST")
def save_album():
	year = request.forms.get("year")
	artist = request.forms.get("artist")
	genre = request.forms.get("genre")
	album = request.forms.get("album")

	try:
		year = int(year)
	except ValueError:
		return HTTPError(400, "Incorrect year")

	try:
		new_album = album.save_new_album(year, artist, genre, album)
	except album.AlreadyInDB as error:
		result = HTTPError(409, str(error))
	else:
		print("New album has been successfully saved by the id {}".format(new_album.id))
		result = "Album {} has been successfully saved by the id {}".format(new_album.album, new_album.id)
	return result

if __name__ == "__main__":
	run(host="localhost", port=8080, debug=True)