from __future__ import absolute_import
from persistence.DAO import UserDAO, MessageDAO
from model.Message import Message
from datetime import datetime
import bcrypt

class MockUserDAO(UserDAO):
    """This is a mock DAO object"""
    def __init__(self):
        self.default_salt = bcrypt.gensalt()
        self.default_hash = bcrypt.hashpw(bytes('123ABC', 'utf-8'), self.default_salt)
        self.users = ['Tarnished', 'Radahn', 'Malenia', 'Melina', 'Morgott']
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
        return bytes(self.salts.get(username, bcrypt.gensalt()))
    
    def checkHash(self, username: str, pass_hash: bytes) -> bool:
        return self.hash.get(username, b'') == pass_hash

    def getUsers(self) -> list:
        return self.users

    def setValues(self, username: str, pass_hash: bytes, salt: bytes) -> None:
        self.salts[username] = salt
        self.hash[username] = pass_hash

    def createUser(self, username: str, pass_hash: bytes, salt: bytes) -> None:
        self.setValues(username, pass_hash, salt)
        self.users.append(username)
    
    def setPassHash(self, username: str, pass_hash: bytes, salt: bytes) -> None:
        self.setValues(username, pass_hash, salt)

    def setUsername(self, old_username, new_username) -> None:
        self.users[self.users.index(old_username)] = new_username
        self.setValues(new_username, self.hash[old_username], self.salts[old_username])
        del self.hash[old_username]
        del self.salts[old_username]

class MockMessageDAO(MessageDAO):
    def __init__(self):
        self.erdtree = {
            1: (1, 'Fools emboldened by the flame of ambition.', False, datetime(2012, 7, 17 ,10, 0, 0), 'Morgott'),
            2: (2, 'My brother in Marika you wear rags and you call yourself "King".', False, datetime(2012, 7, 17, 10, 0, 10), 'Tarnished'),
            3: (3, '*Bodies Morgott*', False, datetime(2012, 7, 17, 10, 3, 0), 'Tarnished'),
            4: (4, 'Literally how. Nah he hacking get him out.', False, datetime(2012, 7, 17, 10, 3, 15), 'Morgott'),
            5: (5, 'L Bozo + mad + skill issue + golden order fell off + go back to the sewers', False, datetime(2012, 7, 17, 10, 3, 20), 'Tarnished')
        }
        self.radahns = {
            6: (6, 'GRARARRHRHHRHHR', False, datetime(2012, 7, 23, 13, 0, 0), 'Radahn'),
            7: (7, 'Bro why is he growling. Ur not him', False, datetime(2012, 7, 23, 13, 0, 5), 'Tarnished'),
            8: (8, 'GUH!!!', False, datetime(2012, 7, 23, 13, 2, 12), 'Radahn'),
            9: (9, '*Bodies Radahn*', False, datetime(2012, 7, 23, 13, 5, 32), 'Tarnished'),
            10: (10, 'Imagine learning gravity magic just to be beat by a guy with a stick.', False, datetime(2012, 7, 23, 13, 5, 45), 'Tarnished')
        }
        self.grand = {}
        self.id_seq = 10

    def retrieveChatroom(self, chatname: str):
        match (chatname):
            case 'Erdtree Sanctuary':
                return self.erdtree
            case 'Radahns Battlefield':
                return self.radahns
            case 'Grand Study Hall':
                return self.grand

    def parseTime(self, timestamp: str):
        date, time = timestamp.split(' ')
        year, month, day = date.split('-')
        hour, minute, second = time.split(':')
        return datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    
    def getMessages(self, chatname: str, args: dict = {}):
        chatroom = self.retrieveChatroom(chatname)
        
        contains = args.get('contains', False)
        after = args.get('after', False)
        before = args.get('before', False)
        username = args.get('username', False)

        if (contains):
            chatroom = {k:v for k,v in chatroom.items() if contains in v[1]}
        if (username):
            chatroom = {k:v for k,v in chatroom.items() if v[4] == username}
        if (after):
            after = self.parseTime(after)
            chatroom = {k:v for k,v in chatroom.items() if v[3] > after}
        if (before):
            before = self.parseTime(before)
            chatroom = {k:v for k,v in chatroom.items() if v[3] < before}

        messages = list(chatroom.values())

        messages.sort(reverse=True, key=lambda x: x[0])

        return messages

    def createMessage(self, chatname: str, message: Message):
        message.timestamp = self.parseTime(message.timestamp)
        self.id_seq += 1
        self.retrieveChatroom(chatname)[self.id_seq] = (self.id_seq, *message.asList())
        return self.id_seq

    def editMessage(self, chatname: str, message: Message):
        chatroom = self.retrieveChatroom(chatname)
        persistMessage = list(chatroom[message.id])
        persistMessage[2] = True
        persistMessage[1] = message.message
        chatroom[message.id] = tuple(persistMessage)

    def deleteMessage(self, chatname: str, id: int):
        chatroom = self.retrieveChatroom(chatname)
        if id in chatroom.keys():
            del chatroom[id]