import json
from typing import Iterable, Union

from ..SETTINGS.SETTINGS import objects_dict


# Request types
GET = 'get'
SHOW = 'show'
HIDE = 'hide'
SEARCH = 'search'
ANSWER = 'answer'

EMPTY_PARCEL = {'type': ANSWER, 'object': '', 'data': {}}


class InParcel:
    def __init__(self, parcel: str, sender) -> None:
        parcel_dict: dict = self._make_dict_from_string(parcel)
        self.type: str = parcel_dict['type']
        self.object_name: str = parcel_dict['object']
        self.data = parcel_dict['data']
        self.sender = sender

    def _make_dict_from_string(self, parcel: str) -> dict:
        return json.loads(parcel)


class OutParcel:
    def __init__(
            self,
            object_name: str,
            destination: Iterable,
            data: Union[dict, None],
            type: str = ANSWER,
    ):
        """
        Arguments:
            object_name - name of object, typically from object.get_name()
            data - data dict to send
            destination - where to send parcel. If one, wrap it to tuple
            type - general purpose requirement, don't change if not needed
        """
        if data is None:
            data = {}
        self.type = type
        self.object_name = object_name
        self.data = data
        self.destination = destination

    def _get_parcel_dict(self):
        data_dict = EMPTY_PARCEL
        data_dict['type'] = self.type
        data_dict['object'] = self.object_name
        data_dict['data'] = self.data
        return data_dict

    def to_json(self):
        return json.dumps(self._get_parcel_dict())

    def __str__(self):
        return f'[OutParcel]: {(self.type, self.object_name, self.data)}'


def handleParcel(parcel: dict, sender) -> OutParcel:
    try:
        inparcel = InParcel(parcel, sender=sender)
    except KeyError:
        return OutParcel(
            object_name='error',
            destination=(sender,),
            data='Can not find required keys'
        )
    return _handleParcel(inparcel)


def _handleParcel(parcel: InParcel) -> OutParcel:
    try:
        from ..DB_objects.CommonObject import CommonObject
        object_to_handle: CommonObject = objects_dict[parcel.object_name]
    except KeyError:
        return OutParcel(
            object_name='error',
            destination=(parcel.sender,),
            data=f'Object {parcel.object_name} is not registered'
        )

    return object_to_handle.handle(parcel)
