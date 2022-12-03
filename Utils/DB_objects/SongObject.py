import json
from .CommonObject import CommonObject


class SongObject(CommonObject):
    _name: str = 'song'

    @classmethod
    def get(cls, parcel):
        from Utils.WSUtils.Parcel import OutParcel
        request = 'SELECT s.id, s.name, s.number FROM Song s'
        songs = cls._exec_req(request)

        ret_dict = {
            'all': [
                {
                    'id': song[0],
                    'fullName': song[1],
                    'mark': song[2]
                } for song in songs
            ]
        }

        return OutParcel(
            cls._name,
            data=ret_dict,
            destination=(parcel.sender,)
        )

    @classmethod
    def create(cls, parcel):
        from Utils.WSUtils.Parcel import InParcel
        song = parcel.data['song']
        c_name: str = song['name']
        c_mark: int = int(song['mark'])

        cr_req = (
            f'INSERT INTO Song (name, name_upper, number) '
            f'VALUES ("{c_name}", "{c_name.upper()}", {c_mark})'
        )
        cls._commit_req(cr_req)

        parcel_to_get_songs = InParcel(
            parcel=json.dumps(
                {
                    'type': '', 'object': '',
                    'data': dict()
                }
            ),
            sender=parcel.sender
        )
        return cls.get(parcel_to_get_songs)

    @classmethod
    def search(cls, parcel):
        from Utils.WSUtils.Parcel import OutParcel, SEARCH

        search_str: str = parcel.data['search_str']

        check_result = cls.check_str_for_search(search_str)
        print(check_result)
        if check_result is not None:
            return OutParcel(
                'error',
                data=check_result,
                destination=(parcel.sender,)
            )

        if cls._check_if_str_is_numbers(search_str):
            request = (
                f'SELECT s.id, s.name, s.number '
                f'FROM Song s '
                f'WHERE s.number = {search_str}'
            )
        else:
            request = (
                f'SELECT s.id, s.name, s.number '
                f'FROM Song s '
                f'WHERE s.name_upper '
                f'LIKE \'%{search_str.upper()}%\''
            )

        songs = cls._exec_req(request)

        if len(songs) == 0:
            ret_dict = {}
        else:
            ret_dict = {
                'found': {
                    'id': songs[0][0],
                    'fullName': songs[0][1],
                    'mark': songs[0][2]
                }
            }

        return OutParcel(
            parcel.object_name,
            data=ret_dict,
            destination=(parcel.sender,),
            type=SEARCH
        )

    @staticmethod
    def _check_if_str_is_numbers(s):
        numbers = set([str(i) for i in range(10)])
        return all([ch in numbers for ch in s])
