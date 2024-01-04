from __future__ import absolute_import
from abc import ABC, abstractmethod
from model.Message import Message

class MessageDAO(ABC):
    
    @abstractmethod
    def getMessages(self, args: dict) -> list:
        """Retrieves messages from persistence following criteria."""
        pass
    
    @abstractmethod
    def createMessage(self, message: Message) -> int:
        """Creates message in persistence while returning reference id."""
        pass

    @abstractmethod
    def deleteMessage(self, id: int) -> None:
        """Deletes message from persistence."""
        pass

    @abstractmethod
    def editMessage(self, message: Message) -> None:
        """Modifies existing message in persistence."""
        pass

class UserDAO(ABC):

    @abstractmethod
    def getSalt(self, username: str) -> bytes:
        """Returns the salt belonging to the user"""
        pass

    @abstractmethod
    def checkHash(self, username: str, pass_hash: bytes) -> bool:
        """Returns whether the password hash matches in persistence"""
        pass

    @abstractmethod
    def getUsers(self) -> list:
        """Returns a list of all users"""
        pass

    @abstractmethod
    def createUser(self, username: str, pass_hash: bytes, salt: bytes) -> None:
        """Creates a user in persistence"""
        pass

    @abstractmethod
    def setPassHash(self, username: str, pass_hash: bytes, salt: bytes) -> None:
        """Replaces pass_hash and salt for existing user"""
        pass

    @abstractmethod
    def setUsername(self, old_username: str, new_username: str) -> None:
        """Changes out the username for an existing user"""
        pass

# TODO: CommunityDAO
# TODO: ChatDAO
