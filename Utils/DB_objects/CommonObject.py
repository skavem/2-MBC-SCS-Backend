from .DB_SQLite3 import DB_SQLite3


class CommonObject():
    _name: str = 'common'

    @classmethod
    def _exec_req(cls, req: str):
        return DB_SQLite3.execute_and_get_data(req)

    @classmethod
    def _commit_req(cls, req: str):
        return DB_SQLite3.execute_and_commit(req)

    @classmethod
    def getname(cls):
        return cls._name

    @classmethod
    def handle(cls, parcel):
        try:
            return getattr(cls, parcel.type)(parcel)
        except AttributeError:
            from ..WSUtils.Parcel import OutParcel
            return OutParcel(
                object_name='error',
                type='error',
                destination=(parcel.sender, ),
                data=f'Method {parcel.type} '
                f'for object {cls.getname()} is not defined'
            )

    @staticmethod
    def check_str_for_restricted_symbols(check_str: str) -> bool:
        restricted_chars = ',.;"\'][<>?{}\\~`-()'
        if any((c in restricted_chars) for c in check_str):
            return True
        return False

    @classmethod
    def check_str_for_search(cls, check_str: str):
        if not len(check_str.replace(' ', '')):
            return {'error': "А как искать? :("}
        if cls.check_str_for_restricted_symbols(check_str):
            return {'error': "Использован запрещенный символ"}
        return None


class ErrorObject(CommonObject):
    __name: str = 'error'
