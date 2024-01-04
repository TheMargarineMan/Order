from __future__ import absolute_import
from unittest import TestCase
from model.User import UserAuth
from test.persistence.mockDAO import MockUserDAO

class TestUser(TestCase):
    users = [
        'Tarnished',
        'Radahn',
        'Malenia',
        'Melina',
        'Morgott'
    ]
    
    def setUp(self):
        self.userAuth = UserAuth(MockUserDAO())

    def testGetUsers(self):
        expected = self.users
        result = self.userAuth.getUsers()
        self.assertEqual(expected, result)

    def testCheckLoginPass(self):
        username = 'Tarnished'
        password = '123ABC'
        self.assertTrue(self.userAuth.checkLogin(username, password))

    def testCheckLoginFail(self):
        username = 'Tarnished'
        password = 'ABC123'
        self.assertFalse(self.userAuth.checkLogin(username, password))

    def testSetUsername(self):
        old_username = 'Tarnished'
        new_username = 'EldenLord'
        password = '123ABC'
        self.userAuth.setUsername(old_username, new_username)
        self.assertFalse(self.userAuth.checkLogin(old_username, password))
        self.assertTrue(self.userAuth.checkLogin(new_username, password))

    def testSetPassword(self):
        username = 'Tarnished'
        old_password = '123ABC'
        new_password = 'ABC123'
        self.userAuth.setPassword(username, new_password)
        self.assertTrue(self.userAuth.checkLogin(username, new_password))
        self.assertFalse(self.userAuth.checkLogin(username, old_password))

    def testCreateUser(self):
        username = 'Radagon'
        password = '123ABC'
        self.userAuth.createUser(username, password)
        self.assertTrue(self.userAuth.checkLogin(username, password))
