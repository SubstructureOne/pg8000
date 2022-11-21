"""WebSocket support"""
import websocket


class WebSocketWrapper:
    """Wrap a WebSocket in a way that roughly resembles a combination of
    a :class:`socket.socket` and the file-like object returned by
    :meth:`socket.socket.makefile`."""
    @classmethod
    def create_connection(cls, host: str, port: int):
        conn = WebSocketWrapper(host, port)
        conn.connect()
        return conn

    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._conn = None
        self._buf: bytearray = bytearray()

    def connect(self):
        url = f'ws://{self._host}:{self._port}'
        self._conn = websocket.create_connection(url)

    def flush(self):
        pass

    def makefile(self, mode):
        return self

    def read(self, numbytes: int):
        while len(self._buf) < numbytes:
            self._buf.extend(self._conn.recv())
        result = self._buf[:numbytes]
        self._buf = self._buf[numbytes:]
        return bytes(result)

    def write(self, data: bytes):
        self._conn.send_binary(data)

    def close(self):
        self._conn.close()

