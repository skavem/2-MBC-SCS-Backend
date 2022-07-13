from Utils.WSUtils.WSStateSingletone import WSStateSingletone
import itertools
from .CommonObject import CommonObject


class RecieverObject(CommonObject):
    _cur_verse_id = None
    _cur_couplet_id = None

    @classmethod
    def show_verse(cls, parcel):
        from Utils.WSUtils.Parcel import OutParcel, SHOW

        cls._cur_verse_id = parcel.data['verse_id']

        ret_dict = cls.get_cur_verse_data_dict()

        return OutParcel(
            object_name='verse',
            data=ret_dict,
            destination=(
                itertools.chain(
                    WSStateSingletone().get_recievers(),
                    WSStateSingletone().get_transmitters()
                )
            ),
            type=SHOW
        )

    @classmethod
    def get_cur_verse_data_dict(cls):
        verse_with_ref = cls._exec_req(
            f"SELECT "
            f"v.text, "
            f"v.number as v_num, "
            f"c.number as c_num, "
            f"b.full_name as book "
            f"FROM Verse v "
            f"JOIN Chapter c on v.chapter_of = c.id "
            f"JOIN Book b on c.book_of = b.abbrev "
            f"WHERE v.id = {cls._cur_verse_id}"
        )[0]
        ret_dict = {
            'verse': {
                'text': verse_with_ref[0],
                'id': cls._cur_verse_id
            },
            'reference': {
                'book': verse_with_ref[3],
                'chapter': verse_with_ref[2],
                'verse': verse_with_ref[1]
            }
        }

        return ret_dict

    @classmethod
    def hide_verse(cls, parcel):
        from Utils.WSUtils.Parcel import OutParcel, HIDE

        cls._cur_verse_id = None

        return OutParcel(
            object_name='verse',
            data={},
            destination=(
                itertools.chain(
                    WSStateSingletone().get_recievers(),
                    WSStateSingletone().get_transmitters()
                )
            ),
            type=HIDE
        )

    @classmethod
    def show_couplet(cls, parcel):
        from Utils.WSUtils.Parcel import OutParcel, SHOW

        cls._cur_couplet_id = parcel.data['couplet_id']

        ret_dict = cls.get_cur_couplet_data_dict()

        return OutParcel(
            object_name='couplet',
            data=ret_dict,
            destination=(
                itertools.chain(
                    WSStateSingletone().get_recievers(),
                    WSStateSingletone().get_transmitters()
                )
            ),
            type=SHOW
        )

    @classmethod
    def get_cur_couplet_data_dict(cls):
        couplet = cls._exec_req(
            f'SELECT c.text '
            f'FROM Couplet c '
            f'WHERE c.id = {cls._cur_couplet_id}'
        )[0]
        ret_dict = {
            'couplet': {
                'text': couplet[0],
                'id': cls._cur_couplet_id
            }
        }

        return ret_dict

    @classmethod
    def hide_couplet(cls, parcel):
        from Utils.WSUtils.Parcel import OutParcel, HIDE

        cls._cur_couplet_id = None

        return OutParcel(
            object_name='couplet',
            data={},
            destination=(
                itertools.chain(
                    WSStateSingletone().get_recievers(),
                    WSStateSingletone().get_transmitters()
                )
            ),
            type=HIDE
        )

    @classmethod
    def get_current_couplet_and_verse_dcit(cls):
        ret_dict = dict()

        if cls._cur_couplet_id is not None:
            ret_dict['couplet'] = cls.get_cur_couplet_data_dict()

        if cls._cur_verse_id is not None:
            ret_dict['verse'] = cls.get_cur_verse_data_dict()

        return ret_dict
