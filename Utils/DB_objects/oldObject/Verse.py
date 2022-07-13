from .DB_common_object import DB_common_object


class Verse(DB_common_object):

    @classmethod
    def get(cls, data):
        search_str = data['verse_search_srt']
        errors = cls.check_str_for_search(search_str)
        if not (errors is None):
            return errors

        ver_req = (
            f"SELECT v.text, v.number, c.number, b.abbrev "
            f"FROM VerseSearch vs "
            f"LEFT JOIN Verse v ON vs.id = v.id "
            f"INNER JOIN Chapter c ON v.chapter_of = c.id "
            f"INNER JOIN Book b ON c.book_of = b.abbrev "
            f"WHERE VerseSearch MATCH '{search_str}' "
            f"ORDER BY rank LIMIT 25"
        )
        verses = cls.exec_req(ver_req).fetchall()
        return {'search_result': verses}

    @classmethod
    def send(cls, data):
        ver_req = (
            f"SELECT v.text FROM Verse v "
            f"WHERE v.chapter_of = ("
            f"SELECT c.id FROM Chapter c "
            f"WHERE c.book_of = '{data['book']}' "
            f"AND c.number = {int(data['ch'])}) "
            f"AND v.number = {int(data['vr'])};"
        )
        verse = cls.exec_req(ver_req).fetchall()[0][0]

        ref_req = (
            f"SELECT b.full_name "
            f"FROM Book b "
            f"WHERE b.abbrev='{data['book']}'"
        )
        ver_ref = (cls.exec_req(ref_req).fetchall()[0][0]
                   + f" {data['ch']}:{data['vr']}")

        return {'verse': verse, 'ref': ver_ref}
