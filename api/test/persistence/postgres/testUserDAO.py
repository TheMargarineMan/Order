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
        expected = 'salt'
        result = self.userDAO.getSalt('Tarnished')
        self.assertEqual(expected, result)

    def testCheckHashTrue(self):
        result = self.userDAO.checkHash('Tarnished', bytes.fromhex('123ABC'))
        self.assertTrue(result)

    def testCheckHashFalse(self):
        result = self.userDAO.checkHash('Tarnished', bytes.fromhex('321CBA'))
        self.assertFalse(result)

    def testSetPassHash(self):
        self.userDAO.setPassHash('Tarnished', bytes.fromhex('321CBA'), 'pepper')
        self.assertEqual('pepper', self.userDAO.getSalt('Tarnished'))
        self.assertTrue(self.userDAO.checkHash('Tarnished', bytes.fromhex('321CBA')))

    def testSetUsername(self):
        self.userDAO.setUsername('Tarnished', 'EldenLord')
        
        expected = self.users
        expected[0] = 'EldenLord'
        result = self.userDAO.getUsers()

        self.assertEqual(expected, result)
   
    def testCreateUser(self):
        self.userDAO.createUser('Radagon', bytes.fromhex('123ABC'), 'salt')
        
        expected = [*self.users, 'Radagon']
        result = self.userDAO.getUsers()

        self.assertEqual(expected, result)
        self.assertTrue(self.userDAO.checkHash('Radagon', bytes.fromhex('123ABC')))
        self.assertEqual('salt', self.userDAO.getSalt('Radagon'))
