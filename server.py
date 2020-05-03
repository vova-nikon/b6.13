from bottle import run
from bottle import route
from bottle import HTTPError
from bottle import request

import album

@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "No albums of {} have been found".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "There are {} albums of {}:<br>".format(len(album_names), artist)
        result += "<br>".join(album_names)
    return result

@route("/albums", method="POST")
def create_album():
    year = request.forms.get("year")
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album_name = request.forms.get("album")

    try:
        year = int(year)
    except:
        return HTTPError(400, "The year is incorrect")

    try:
        new_album = album.save_new(year, artist, genre, album_name)
    except AssertionError as err:
        result = HTTPError(400, str(err))
    except album.AlreadyInDB as err:
        result = HTTPError(409, str(err))
    else:
        print("The album {} has successfully been saved by the id {}".format(new_album.album, new_album.id))
        result = "The album {} has successfullybeen saved by the id {}".format(new_album.album, new_album.id)
    return result

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
