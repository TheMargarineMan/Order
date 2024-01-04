from __future__ import absolute_import
import bcrypt
from persistence.DAO import UserDAO

class UserAuth():

    def __init__(self, dao: UserDAO):
        self.dao = dao

    def getUsers(self) -> list:
        return self.dao.getUsers()

    def checkLogin(self, username: str, password: str):
        salt = self.dao.getSalt(username)
        pass_hash = bcrypt.hashpw(bytes(password, 'utf-8'), salt)
        return self.dao.checkHash(username, pass_hash)

    def setUsername(self, old_username: str, new_username: str):
        self.dao.setUsername(old_username, new_username)

    def setPassword(self, username: str, new_password: str):
        new_salt = bcrypt.gensalt()
        new_hash = bcrypt.hashpw(bytes(new_password, 'utf-8'), new_salt)
        self.dao.setPassHash(username, new_hash, new_salt)

    def createUser(self, username: str, password: str):
        salt = bcrypt.gensalt()
        pass_hash = bcrypt.hashpw(bytes(password, 'utf-8'), salt)
        self.dao.createUser(username, pass_hash, salt)