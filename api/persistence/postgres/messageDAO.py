from ..DAO import MessageDAO
from ...model.Message import Message
from .__init__ import CONNPOOL, exec_get,

class PostgresMessageDAO(MessageDAO):

    def __init__(self):
        pass

    def getMessages(args: dict) -> list:
        pass
    
    def getMessage(id: int) -> Message:
        pass

    def createMessage(message: Message) -> int:
        pass

    def deleteMessage(id: int) -> None:
        pass

    def editMessage(message: Message) -> Message:
        pass
