from __future__ import absolute_import
from unittest import TestCase
from datetime import datetime
from test.persistence.mockDAO import MockMessageDAO
from test.persistence.testMessageDAO import TestMessageDAO
from persistence.postgres.messageDAO import PostgresMessageDAO
from persistence.postgres.__init__ import exec_file, exec_commit
from model.Message import Message

class TestPostgresMessageDAO(TestMessageDAO):
    
    @classmethod
    def setUpClass(self):
        # Loads test data destructively
        TestMessageDAO.resetFile = 'api/test/persistence/postgres/testData.sql'
        TestMessageDAO.messageDAO = PostgresMessageDAO()
        
    @classmethod
    def tearDownClass(self):
        # Destroys all test data
        exec_commit("""
            DELETE FROM messages;
            DELETE FROM chats;
            DELETE FROM users;
        """)
    
    def setUp(self):
        exec_file(TestMessageDAO.resetFile)
