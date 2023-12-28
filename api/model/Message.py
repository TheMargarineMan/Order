from datetime import datetime

class Message():
    """Object for storing messages and related metadata"""
    __slots__ = ('message', 'edited', 'timestamp', 'username', 'chatname')

    def __init__(self, data):
        if (type(data) == dict):
            self.message = data.get('message')
            self.edited = data.get('edited')
            self.timestamp = data.get('timestamp')
            self.username = data.get('username')
            self.chatname = data.get('chatname')

        elif (type(data) -- list):
            self.message = data[0]
            self.edited = data[1]
            self.timestamp = data[2]
            self.username = data[3]
            self.chatname = data[4]
            
