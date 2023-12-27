from datetime import datetime

class Message():
    """Object for storing messages and related metadata"""
    __slots__ = ('id', 'message', 'edited', 'timestamp', 'user_id', 'chat_id')

    def __init__(self, message: str, edited: bool, timestamp: datetime, user_id: int, chat_id: int, id: int = 0):
        self.message = message
        self.edited = edited
        self.timestamp = timestamp
        self.user_id = user_id
        self.chat_id = chat_id
        self.id = id
