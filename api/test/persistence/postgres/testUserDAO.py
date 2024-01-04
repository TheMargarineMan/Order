from __future__ import absolute_import
from unittest import TestCase
from persistence.postgres.userDAO import PostgresUserDAO
from persistence.postgres.__init__ import exec_file, exec_commit

class TestPostgresChatDAO(TestCase):

    users = [
        'Tarnished',
        'Radahn',
        'Malenia',
        'Melina',
        'Morgott'
    ]
    
    @classmethod
    def setUpClass(self):
        # Loads test data destructively
        self.resetFile = 'api/test/persistence/postgres/testData.sql'
        self.userDAO = PostgresUserDAO()
        
    @classmethod
    def tearDownClass(self):
        # Destroys all test data
        exec_commit("""
            DELETE FROM messages;
            DELETE FROM chats;
            DELETE FROM users;
        """)
    
    def setUp(self):
        exec_file(self.resetFile)

    def testGetUsers(self):
        expected = self.users
        result = self.userDAO.getUsers()
        self.assertEqual(expected, result)

    def testGetSalt(self):
        expected = bytes('salt', 'utf-8')
        result = self.userDAO.getSalt('Tarnished')
        self.assertEqual(expected, result)

    def testCheckHashTrue(self):
        result = self.userDAO.checkHash('Tarnished', bytes.fromhex('123ABC'))
        self.assertTrue(result)

    def testCheckHashFalse(self):
        result = self.userDAO.checkHash('Tarnished', bytes.fromhex('321CBA'))
        self.assertFalse(result)

    def testSetPassHash(self):
        newSalt = b'pepper'
        newHash = bytes.fromhex('321CBA')
        self.userDAO.setPassHash('Tarnished', newHash, newSalt)
        self.assertEqual(newSalt, self.userDAO.getSalt('Tarnished'))
        self.assertTrue(self.userDAO.checkHash('Tarnished', newHash))

    def testSetUsername(self):
        self.userDAO.setUsername('Tarnished', 'EldenLord')
        
        expected = self.users
        expected[0] = 'EldenLord'
        result = self.userDAO.getUsers()

        self.assertEqual(expected, result)
   
    def testCreateUser(self):
        username = 'Radagon'
        pass_hash = bytes.fromhex('123ABC')
        salt = b'salt'

        self.userDAO.createUser(username, pass_hash, salt)
        
        expected = [*self.users, username]
        result = self.userDAO.getUsers()

        self.assertEqual(expected, result)
        self.assertTrue(self.userDAO.checkHash(username, pass_hash))
        self.assertEqual(salt, self.userDAO.getSalt(username))
