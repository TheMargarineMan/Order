from datetime import datetime

class Message():
    """Object for storing messages and related metadata"""
    __slots__ = ('id', 'message', 'edited', 'timestamp', 'username')

    def __init__(self, data):
        if (type(data) == dict):
            self.id = data.get('id', None)
            self.message = data.get('message')
            self.edited = data.get('edited')
            self.timestamp = data.get('timestamp')
            self.username = data.get('username')

        elif (type(data) == list):
            self.id = data[0]
            self.message = data[1]
            self.edited = data[2]
            self.timestamp = data[3]
            self.username = data[4]

    def asList(self) -> list:
        return [
            self.message,
            self.edited,
            self.timestamp,
            self.username
        ]
