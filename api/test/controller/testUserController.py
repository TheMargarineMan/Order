from __future__ import absolute_import
from .__init__ import userController, testHttpRequest
from unittest import TestCase
from fastapi import HTTPException
from fastapi.testclient import TestClient
from test.persistence.mockDAO import MockUserDAO

class TestUserController(TestCase):
    users = [
        'Tarnished',
        'Radahn',
        'Malenia',
        'Melina',
        'Morgott'
    ]

    def setUp(self):
        userController.assignDAO(MockUserDAO())

    def testLoginPass(self):
        username = 'Tarnished'
        password = '123ABC'

        # Attempt Login
        testHttpRequest(self, '/login', 'POST', \
                        {}, \
                        {'username': username, 'password': password})

    def testLoginFail(self):
        username = 'Tarnished'
        password = 'ABC123'

        # Attempt Login
        testHttpRequest(self, '/login', 'POST', \
                        {}, \
                        {'username': username, 'password': password}, \
                        403)

    def testChangePassword(self):
        username = 'Tarnished'
        old_password = '123ABC'
        new_password = 'ABC123'
        
        # Attempt Password Change
        testHttpRequest(self, '/login', 'PUT', \
                        {'username': username}, \
                        {'old_password': old_password, 'new_password': new_password})

        # Attempt Login (new_password)
        testHttpRequest(self, '/login', 'POST', \
                        {}, \
                        {'username': username, 'password': new_password})

        # Attempt Login (old_password)
        testHttpRequest(self, '/login', 'POST', \
                        {}, \
                        {'username': username, 'password': old_password}, \
                        403)
        
    def testChangePasswordFail(self):
        username = 'Tarnished'
        bad_password = 'ABCABC'

        # Attempt Password Change
        testHttpRequest(self, '/login', 'PUT', \
                        {'username': username}, \
                        {'old_password': bad_password, 'new_password': bad_password}, \
                        403)

    def testGetUsers(self):
        expected = self.users
        result = testHttpRequest(self, '/users', 'GET', {}, {})
        self.assertEqual(expected, result)
    
    def testChangeUsername(self):
        old_username = 'Tarnished'
        new_username = 'EldenLord'
        password = '123ABC'

        # Attempt Username Change
        testHttpRequest(self, '/users', 'PUT', \
                        {'username': old_username}, \
                        {'username': new_username, 'password': password})

        # Verify Full Userlist
        expected = ['EldenLord', *self.users[1:]]
        result = testHttpRequest(self, '/users', 'GET', {}, {})
        self.assertEqual(expected, result)

        # Attempt Login (old_username)
        testHttpRequest(self, '/login', 'POST', \
                        {}, \
                        {'username': old_username, 'password': password}, \
                        403)

        # Attempt Login (new_username)
        testHttpRequest(self, '/login', 'POST', \
                        {}, \
                        {'username': new_username, 'password': password})

    def testChangeUsernameFail(self):
        old_username = 'Tarnished'
        new_username = 'EldenLord'
        bad_password = 'ABCABC'

        # Attempt Username Change
        testHttpRequest(self, '/users', 'PUT', \
                        {'username': old_username}, \
                        {'username': new_username, 'password': bad_password}, \
                        403)

    def testRegister(self):
        username = 'Radagon'
        password = '2ndConsort'

        # Attempt Register
        testHttpRequest(self, '/register', 'POST', \
                        {}, \
                        {'username': username, 'password': password}, \
                        201)

        # Attempt Login
        testHttpRequest(self, '/login', 'POST', \
                        {}, \
                        {'username': username, 'password': password})

        # Verify Full Userlist
        expected = [*self.users, 'Radagon']
        result = testHttpRequest(self, '/users', 'GET', {}, {})
        self.assertEqual(expected, result)


