from abc import ABC, abstractmethod
from ..model.Message import Message

class MessageDAO(ABC):
    
    @abstractmethod
    def getMessage(id: int) -> Message:
        """Retrieves message from persistence returning contents."""
        pass

    @abstractmethod
    def getMessages(args: dict) -> list:
        """Retrieves messages from persistence following criteria."""
        pass
    
    @abstractmethod
    def createMessage(message: Message) -> int:
        """Creates message in persistence while returning reference id."""
        pass

    @abstractmethod
    def deleteMessage(id: int) -> None:
        """Deletes message from persistence."""
        pass

    @abstractmethod
    def editMessage(message: Message) -> Message:
        """Modifies existing message in persistence, returning modified message."""
        pass
    

# TODO: UserDAO/User Auth Utils

# TODO: CommunityDAO
# TODO: ChatDAO
