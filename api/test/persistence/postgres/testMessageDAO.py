from __future__ import absolute_import
from unittest import TestCase
from datetime import datetime
from persistence.postgres.messageDAO import PostgresMessageDAO
from persistence.postgres.__init__ import exec_file, exec_commit

class TestPostgresMessageDAO(TestCase):

    data = [
        ('Fools emboldened by the flame of ambition.', False, datetime(2012, 7, 17 ,10, 0, 0), 'Morgott', 'Erdtree Sanctuary'),
        ('My brother in Marika you wear rags and you call yourself "King".', False, datetime(2012, 7, 17, 10, 0, 10), 'Tarnished', 'Erdtree Sanctuary'),
        ('*Bodies Morgott*', False, datetime(2012, 7, 17, 10, 3, 0), 'Tarnished', 'Erdtree Sanctuary'),
        ('Literally how. Nah he hacking get him out.', False, datetime(2012, 7, 17, 10, 3, 15), 'Morgott', 'Erdtree Sanctuary'),
        ('L Bozo + mad + skill issue + golden order fell off + go back to the sewers', False, datetime(2012, 7, 17, 10, 3, 20), 'Tarnished', 'Erdtree Sanctuary'),
        ('GRARARRHRHHRHHR', False, datetime(2012, 7, 23, 13, 0, 0), 'Radahn', 'Radahns Battlefield'),
        ('Bro why is he growling. Ur not him', False, datetime(2012, 7, 23, 13, 0, 5), 'Tarnished', 'Radahns Battlefield'),
        ('GUH!!!', False, datetime(2012, 7, 23, 13, 2, 12), 'Radahn', 'Radahns Battlefield'),
        ('*Bodies Radahn*', False, datetime(2012, 7, 23, 13, 5, 32), 'Tarnished', 'Radahns Battlefield'),
        ('Imagine learning gravity magic just to be beat by a guy with a stick.', False, datetime(2012, 7, 23, 13, 5, 45), 'Tarnished', 'Radahns Battlefield')
    ]

    @classmethod
    def setUpClass(self):
        exec_file('test/persistence/postgres/testData.sql')
        self.messageDAO = PostgresMessageDAO()
        
    @classmethod
    def tearDownClass(self):
        exec_commit("""DELETE FROM messages;
                    DELETE FROM chats;
                    DELETE FROM users;""")

    def testGetMessagesChatOne(self):
        args = { 'chatname': 'Erdtree Sanctuary' }

        expected = self.data[4::-1]
        result = self.messageDAO.getMessages(args)

        self.assertEqual(expected, result)

    def testGetMessagesChatTwo(self):
        args = { 'chatname': 'Grand Study Hall' }

        result = self.messageDAO.getMessages(args)

        self.assertTrue(len(result) == 0)

    def testGetMessagesChatThree(self):
        args = { 'chatname': 'Radahns Battlefield' }

        expected = self.data[:4:-1]
        result = self.messageDAO.getMessages(args)

        self.assertEqual(expected, result)

    def testGetMessageContains(self):
        args = { 'chatname': 'Erdtree Sanctuary', 'contains': 'f' }
        
        expected = [self.data[4], self.data[1], self.data[0]]
        result = self.messageDAO.getMessages(args)

        self.assertEqual(expected, result)

    def testGetMessageUser(self):
        args = { 'chatname': 'Erdtree Sanctuary', 'username': 'Morgott' }
        
        expected = [self.data[3], self.data[0]]
        result = self.messageDAO.getMessages(args)
    
        self.assertEqual(expected, result)

    def testGetMessageBefore(self):
        args = { 'chatname': 'Erdtree Sanctuary', 'before': datetime(2012, 7, 17, 10, 3, 10) }
        
        expected = self.data[2::-1]
        result = self.messageDAO.getMessages(args)
    
        self.assertEqual(expected, result)

    def testGetMessageAfter(self):
        args = { 'chatname': 'Erdtree Sanctuary', 'after': datetime(2012, 7, 17, 10, 3, 10) }
        
        expected = self.data[4:2:-1]
        result = self.messageDAO.getMessages(args)
    
        self.assertEqual(expected, result)
