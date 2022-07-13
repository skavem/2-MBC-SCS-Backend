from .CommonObject import CommonObject


class BookObject(CommonObject):

    @classmethod
    def get(cls, parcel):
        from Utils.WSUtils.Parcel import OutParcel
        request = 'SELECT b.abbrev, b.full_name FROM Book b;'
        books = cls._exec_req(request)
        ret_dict = {
            'all': [
                {'id': book[0], 'fullName': book[1]} for book in books
            ]
        }

        return OutParcel(
            parcel.object_name,
            data=ret_dict,
            destination=(parcel.sender,)
        )
