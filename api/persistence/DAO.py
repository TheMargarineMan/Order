from __future__ import absolute_import
from abc import ABC, abstractmethod
from model.Message import Message

class MessageDAO(ABC):
    
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
    def editMessage(message: Message) -> None:
        """Modifies existing message in persistence."""
        pass

class UserDAO(ABC):

    @abstractmethod
    def getSalt(username: str) -> str:
        """Returns the salt belonging to the user"""
        pass

    @abstractmethod
    def checkHash(username: str, pass_hash: bytes) -> bool:
        """Returns whether the password hash matches in persistence"""
        pass

    @abstractmethod
    def getUsers() -> list:
        """Returns a list of all users"""
        pass

    @abstractmethod
    def createUser(username: str, pass_hash: bytes, salt: str) -> None:
        """Creates a user in persistence"""
        pass

    @abstractmethod
    def setPassHash(username: str, pass_hash: bytes, salt: str) -> None:
        """Replaces pass_hash and salt for existing user"""
        pass

    @abstractmethod
    def setUsername(old_username: str, new_username: str) -> None:
        """Changes out the username for an existing user"""
        pass

# TODO: CommunityDAO
# TODO: ChatDAO
