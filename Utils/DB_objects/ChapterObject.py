from .CommonObject import CommonObject


class ChapterObject(CommonObject):

    @classmethod
    def get(cls, parcel):
        from Utils.WSUtils.Parcel import OutParcel
        request = (
            f"SELECT c.id, c.number "
            f"FROM Chapter c "
            f"WHERE c.book_of = '{parcel.data['book_id']}'")
        chapters = cls._exec_req(request)
        ret_dict = {
            'all': [
                {
                    'id': chapter[0],
                    'fullName': chapter[1]
                } for chapter in chapters
            ]
        }

        return OutParcel(
            parcel.object_name,
            data=ret_dict,
            destination=(parcel.sender,)
        )
