class WSState:
    def __init__(self):
        self._recievers = set()
        self._transmitters = set()

    def add_recv(self, recv):
        self._recievers.add(recv)

    def remove_recv(self, recv):
        self._recievers.discard(recv)

    def get_recievers(self):
        return self._recievers

    def add_trans(self, trans):
        self._transmitters.add(trans)

    def remove_trans(self, trans):
        self._transmitters.remove(trans)

    def get_transmitters(self):
        return self._transmitters


class WSStateSingletone:
    _state: WSState = None

    def __new__(cls):
        if cls._state is None:
            cls._state = WSState()
        return cls._state
