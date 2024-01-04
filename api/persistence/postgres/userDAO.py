from __future__ import absolute_import
from persistence.DAO import UserDAO
from .__init__ import *

class PostgresUserDAO(UserDAO):

    def getUsers(self) -> list:
        query = """
            SELECT username
            FROM users
            ORDER BY id ASC;
        """
        # List comprehension is to extract usernames from returned tuples
        return [n[0] for n in exec_get_all(query)]

    def createUser(self, username: str, pass_hash: bytes, salt: bytes) -> None:
        query = """
            INSERT INTO users(username, pass_hash, salt)
            VALUES (%s, %s, %s);
        """
        return exec_commit(query, (username, pass_hash, salt))

    def setPassHash(self, username: str, pass_hash: bytes, salt: bytes) -> None:
        query = """
            UPDATE users
            SET pass_hash = %s, salt = %s
            WHERE username = %s;
        """
        return exec_commit(query, (pass_hash, salt, username))

    def setUsername(self, old_username: str, new_username: str) -> None:
        query = """
            UPDATE users
            SET username = %s
            WHERE username = %s;
        """
        return exec_commit(query, (new_username, old_username))

    def getSalt(self, username: str) -> str:
        query = """
            SELECT salt
            FROM users
            WHERE username = %s;
        """
        return exec_get_one(query, (username,))[0]

    def checkHash(self, username: str, pass_hash: bytes) -> bool:
        query = """
            SELECT pass_hash = %s
            FROM users
            WHERE username = %s;
        """
        return exec_get_one(query, (pass_hash, username))[0]
