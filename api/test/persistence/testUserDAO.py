from __future__ import absolute_import
from unittest import TestCase
from test.persistence.mockDAO import MockUserDAO

class TestUserDAO(TestCase):
    """
    This test class is for the testing of implementations of UserDAO.
    This test class by default tests the MockUserDAO implementation.
    This test class can be inherited in order to perform tests on other
    implementations of UserDAO, as long as the setUp(), setUpClass() 
    and tearDownClass() methods are properly defined in the child tester.
    """

    users = [
        'Tarnished',
        'Radahn',
        'Malenia',
        'Melina',
        'Morgott'
    ]
    
    def setUp(self):
        self.userDAO = MockUserDAO()
        self.default_hash = self.userDAO.default_hash
        self.default_salt = self.userDAO.default_salt

    def testGetUsers(self):
        expected = self.users
        result = self.userDAO.getUsers()
        self.assertEqual(expected, result)

    def testGetSalt(self):
        expected = self.default_salt
        result = self.userDAO.getSalt('Tarnished')
        self.assertEqual(expected, result)

    def testCheckHashTrue(self):
        result = self.userDAO.checkHash('Tarnished', self.default_hash)
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
        
        expected = ['EldenLord', *self.users[1:]]
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
