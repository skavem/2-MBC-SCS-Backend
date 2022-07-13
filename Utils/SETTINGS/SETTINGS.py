from Utils.DB_objects.ChapterObject import ChapterObject
from Utils.DB_objects.CoupletObject import CoupletObject
from Utils.DB_objects.DB_SQLite3 import DB_SQLite3
from Utils.DB_objects.BookObject import BookObject
from Utils.DB_objects.AuthObject import AuthObject
from Utils.DB_objects.RecieverObject import RecieverObject
from Utils.DB_objects.VerseObject import VerseObject
from Utils.DB_objects.SongObject import SongObject

objects_dict = {
    'book': BookObject,
    'chapter': ChapterObject,
    'verse': VerseObject,

    'song': SongObject,
    'couplet': CoupletObject,

    'reciever': RecieverObject,

    'auth': AuthObject
}

DB_connection = DB_SQLite3
