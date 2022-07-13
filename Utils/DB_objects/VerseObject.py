from .CommonObject import CommonObject
import sqlite3


class VerseObject(CommonObject):

    @classmethod
    def get(cls, parcel):
        from Utils.WSUtils.Parcel import OutParcel

        request = (
            f"SELECT v.id, v.number, v.text FROM Chapter c "
            f"JOIN Verse v ON v.chapter_of = c.id "
            f"WHERE c.id = {int(parcel.data['ch_id'])} "
            f"ORDER BY c.number")
        verses = cls._exec_req(request)

        ret_dict = {
            'all': [
                {
                    'id': verse[0],
                    'mark': verse[1],
                    'fullName': verse[2]
                } for verse in verses
            ]
        }

        return OutParcel(
            parcel.object_name,
            data=ret_dict,
            destination=(parcel.sender,)
        )

    @classmethod
    def search(cls, parcel):
        from Utils.WSUtils.Parcel import OutParcel, SEARCH

        srch_str = parcel.data['search_str']

        if (err := cls.check_str_for_search(srch_str)) is not None:
            return OutParcel(
                'error',
                data=err,
                destination=(parcel.sender,),
            )

        request = (
            f"SELECT v.text, c.number, v.number, b.abbrev, c.id, v.id "
            f"FROM VerseSearch vs "
            f"JOIN Verse v ON vs.id = v.id "
            f"JOIN Chapter c ON c.id = v.chapter_of "
            f"JOIN Book b on c.book_of = b.abbrev "
            f"WHERE VerseSearch MATCH '{srch_str}' "
            f"ORDER BY rank LIMIT 25"
        )
        try:
            verses = cls._exec_req(request)
        except sqlite3.OperationalError as e:
            return OutParcel(
                'error',
                data=f'Ошибка поиска: {str(e)}',
                destination=(parcel.sender,),
            )

        ret_dict = {
            'all': [
                {
                    'fullName': verse[0],
                    'mark': f"{verse[3]} {verse[1]}:{verse[2]}",
                    'book_id': verse[3],
                    'chapter_id': verse[4],
                    'id': verse[5]
                } for verse in verses
            ]
        }

        return OutParcel(
            parcel.object_name,
            data=ret_dict,
            destination=(parcel.sender,),
            type=SEARCH
        )
