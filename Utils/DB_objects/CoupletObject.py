import json
from .CommonObject import CommonObject


class CoupletObject(CommonObject):
    _name: str = 'couplet'

    @classmethod
    def get(cls, parcel):
        from Utils.WSUtils.Parcel import OutParcel
        request = (
            f'SELECT s_c.couplet_id, c.text, c.name '
            f'FROM Song_Couplet s_c '
            f'JOIN Couplet c ON s_c.couplet_id = c.id '
            f'WHERE s_c.song_id = {parcel.data["song_id"]} '
            f'ORDER BY s_c.number'
        )
        couplets = cls._exec_req(request)

        ret_dict = {
            'all': [
                {
                    'id': couplet[0],
                    'fullName': couplet[1],
                    'mark': couplet[2]
                } for couplet in couplets
            ]
        }

        return OutParcel(
            cls._name,
            data=ret_dict,
            destination=(parcel.sender,)
        )

    @classmethod
    def edit(cls, parcel):
        couplet: dict = parcel.data['couplet']
        couplet_text: str = "{}".format(
            couplet["fullName"].replace("\'", r"\'")
        )
        request = (
            f'UPDATE Couplet '
            f'SET '
            f'name = "{couplet["mark"]}", '
            f'text = \'{couplet_text}\' '
            f'WHERE id = {int(couplet["id"])}'
        )
        cls._commit_req(request)

        song_id = cls._exec_req(
            f'SELECT song_id FROM Song_Couplet '
            f'WHERE couplet_id = {couplet["id"]}'
        )[0][0]

        return cls.get_parcel_with_song(song_id, parcel.sender)

    @classmethod
    def insert(cls, parcel):
        couplet = parcel.data['couplet']
        song_id = int(couplet['song_id'])
        insert_after_id = int(couplet["insert_after"])
        couplet_text: str = "{}".format(
            couplet["fullName"].replace("\'", r"\'")
        )
        if (c_i := couplet.get('id')) is None:
            cr_req = (
                f'INSERT INTO Couplet (name, text)'
                f'VALUES ("{couplet["mark"]}", \'{couplet_text}\')'
            )
            couplet_id = cls._commit_req(cr_req)
        else:
            couplet_id = c_i
            del_req = (
                f'DELETE FROM Song_Couplet '
                f'WHERE couplet_id = {couplet_id}'
            )
            cls._commit_req(del_req)

        if insert_after_id == -1:
            ins_after_num = -1
        else:
            getpos_req = (
                f'SELECT number FROM Song_Couplet '
                f'WHERE couplet_id = {insert_after_id}'
            )
            ins_after_num = int(cls._exec_req(getpos_req)[0][0])

        rearr_req = (
            f'UPDATE Song_Couplet SET number = number + 1 '
            f'WHERE song_id = {song_id} '
            f'AND number > {ins_after_num}'
        )
        cls._commit_req(rearr_req)

        ins_req = (
            f'INSERT INTO Song_Couplet (song_id, couplet_id, number) '
            f'VALUES ( '
            f'{song_id}, {couplet_id}, {ins_after_num + 1} '
            f')'
        )
        cls._commit_req(ins_req)

        return cls.get_parcel_with_song(song_id, parcel.sender)

    @classmethod
    def delete(cls, parcel):
        c_id = int(parcel.data["couplet_id"])
        song_id = cls._exec_req(
            f'SELECT sc.song_id '
            f'FROM Song_Couplet sc '
            f'WHERE sc.couplet_id = {c_id}'
        )[0][0]
        del_req = (
            f'DELETE FROM Couplet '
            f'WHERE id = {c_id}'
        )
        cls._commit_req(del_req)

        del_req = (
            f'DELETE FROM Song_Couplet '
            f'WHERE couplet_id = {c_id}'
        )
        cls._commit_req(del_req)

        return cls.get_parcel_with_song(song_id, parcel.sender)

    @classmethod
    def get_parcel_with_song(cls, song_id, sender):
        from Utils.WSUtils.Parcel import InParcel
        parcel_to_update_song = InParcel(
            parcel=json.dumps(
                {
                    'type': '', 'object': '',
                    'data': {'song_id': song_id}
                }
            ),
            sender=sender
        )

        return cls.get(parcel_to_update_song)
