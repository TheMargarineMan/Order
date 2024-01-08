from __future__ import absolute_import
from unittest import TestCase
from test.persistence.testUserDAO import TestUserDAO
from persistence.postgres.userDAO import PostgresUserDAO
from persistence.postgres.__init__ import exec_file, exec_commit

class TestPostgresUserDAO(TestUserDAO):

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
        self.default_salt = bytes('salt', 'utf-8')
        self.default_hash = bytes.fromhex('123ABC')
        
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
