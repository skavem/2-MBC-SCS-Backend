from .CommonObject import CommonObject
from Utils.WSUtils.WSStateSingletone import WSStateSingletone


class AuthObject(CommonObject):
    @classmethod
    def transmitter(cls, parcel):
        from Utils.WSUtils.Parcel import OutParcel
        from Utils.DB_objects.RecieverObject import RecieverObject

        WSStateSingletone().add_trans(parcel.sender)

        couplet_and_verse = RecieverObject.get_current_couplet_and_verse_dcit()

        return OutParcel(
            parcel.object_name,
            data={'status': 'OK GRAPE', **couplet_and_verse},
            destination=(parcel.sender,)
        )

    @classmethod
    def reciever(cls, parcel):
        from Utils.WSUtils.Parcel import OutParcel
        from Utils.DB_objects.RecieverObject import RecieverObject

        WSStateSingletone().add_recv(parcel.sender)

        couplet_and_verse = RecieverObject.get_current_couplet_and_verse_dcit()

        return OutParcel(
            parcel.object_name,
            data={'status': 'OK GRAPE', **couplet_and_verse},
            destination=(parcel.sender,)
        )
