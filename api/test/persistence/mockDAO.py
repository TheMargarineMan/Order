from __future__ import absolute_import
from persistence.DAO import UserDAO
import bcrypt

class MockUserDAO(UserDAO):
    """This is a mock DAO object"""
    def __init__(self):
        self.default_salt = bcrypt.gensalt()
        self.default_hash = bcrypt.hashpw(bytes('123ABC', 'utf-8'), self.default_salt)
        self.salts = {
            'Tarnished': self.default_salt,
            'Radahn': self.default_salt,
            'Malenia': self.default_salt,
            'Melina': self.default_salt,
            'Morgott': self.default_salt
        }
        self.hash = {
            'Tarnished': self.default_hash,
            'Radahn': self.default_hash,
            'Malenia': self.default_hash,
            'Melina': self.default_hash,
            'Morgott': self.default_hash
        }

    def getSalt(self, username: str) -> bytes:
        return bytes(self.salts[username])
    
    def checkHash(self, username: str, pass_hash: bytes) -> bool:
        return self.hash[username] == pass_hash

    def getUsers(self) -> list:
        return list(self.salts.keys())

    def setValues(self, username: str, pass_hash: bytes, salt: bytes) -> None:
        self.salts[username] = salt
        self.hash[username] = pass_hash

    def createUser(self, username: str, pass_hash: bytes, salt: bytes) -> None:
        self.setValues(username, pass_hash, salt)
    
    def setPassHash(self, username: str, pass_hash: bytes, salt: bytes) -> None:
        self.setValues(username, pass_hash, salt)

    def setUsername(self, old_username, new_username) -> None:
        self.setValues(new_username, self.hash[old_username], self.salts[old_username])
        self.setValues(old_username, b'', bcrypt.gensalt())
