import sqlite3


class DB_SQLite3:
    _cur: sqlite3.Cursor = None
    _con: sqlite3.Connection = None

    def __new__(cls):
        if cls._cur is None:
            cls._con = sqlite3.connect('local-remaster.db')
            cls._cur = cls._con.cursor()
        return cls._cur

    @classmethod
    def get_cur(cls) -> sqlite3.Cursor:
        return cls._cur

    @classmethod
    def execute_and_get_data(cls, req):
        return cls._cur.execute(req).fetchall()

    @classmethod
    def execute_and_commit(cls, req):
        cls._cur.execute(req)
        cls._con.commit()
        return cls._cur.lastrowid

    @classmethod
    def close_connection(cls):
        cls._con.close()
