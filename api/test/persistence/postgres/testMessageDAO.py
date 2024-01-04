from __future__ import absolute_import
from unittest import TestCase
from datetime import datetime
from persistence.postgres.messageDAO import PostgresMessageDAO
from persistence.postgres.__init__ import exec_file, exec_commit
from model.Message import Message

class TestPostgresMessageDAO(TestCase):

    data = [
        (1, 'Fools emboldened by the flame of ambition.', False, datetime(2012, 7, 17 ,10, 0, 0), 'Morgott', 'Erdtree Sanctuary'),
        (2, 'My brother in Marika you wear rags and you call yourself "King".', False, datetime(2012, 7, 17, 10, 0, 10), 'Tarnished', 'Erdtree Sanctuary'),
        (3, '*Bodies Morgott*', False, datetime(2012, 7, 17, 10, 3, 0), 'Tarnished', 'Erdtree Sanctuary'),
        (4, 'Literally how. Nah he hacking get him out.', False, datetime(2012, 7, 17, 10, 3, 15), 'Morgott', 'Erdtree Sanctuary'),
        (5, 'L Bozo + mad + skill issue + golden order fell off + go back to the sewers', False, datetime(2012, 7, 17, 10, 3, 20), 'Tarnished', 'Erdtree Sanctuary'),
        (6, 'GRARARRHRHHRHHR', False, datetime(2012, 7, 23, 13, 0, 0), 'Radahn', 'Radahns Battlefield'),
        (7, 'Bro why is he growling. Ur not him', False, datetime(2012, 7, 23, 13, 0, 5), 'Tarnished', 'Radahns Battlefield'),
        (8, 'GUH!!!', False, datetime(2012, 7, 23, 13, 2, 12), 'Radahn', 'Radahns Battlefield'),
        (9, '*Bodies Radahn*', False, datetime(2012, 7, 23, 13, 5, 32), 'Tarnished', 'Radahns Battlefield'),
        (10, 'Imagine learning gravity magic just to be beat by a guy with a stick.', False, datetime(2012, 7, 23, 13, 5, 45), 'Tarnished', 'Radahns Battlefield')
    ]

    @classmethod
    def setUpClass(self):
        # Loads test data destructively
        self.resetFile = 'api/test/persistence/postgres/testData.sql'
        self.messageDAO = PostgresMessageDAO()
        
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

    def testGetMessageGarbageParam(self):
        args = { 'chatname': 'Erdtree Sanctuary', 'garbage': 'garbage' }

        expected = self.data[4::-1]
        result = self.messageDAO.getMessages(args)

        self.assertEqual(expected, result)

    def testCreateMessage(self):
        message = Message({
            "message": "Shadow Wizard Money Gang",
            "edited": False,
            "timestamp": datetime(2012, 7, 18, 10, 0, 0),
            "username": "Melina",
            "chatname": "Grand Study Hall"
        })

        # Test if returned id was as expected        
        result = self.messageDAO.createMessage(message)
        expected = 11
        
        self.assertEqual(expected, result)

        # Test existence in chatroom
        args = { "chatname": "Grand Study Hall" }
            
        expected = [(11, "Shadow Wizard Money Gang", False, datetime(2012, 7, 18, 10, 0, 0), "Melina", "Grand Study Hall")]
        result = self.messageDAO.getMessages(args)

        self.assertEqual(expected, result)

    def testDeleteMessage(self):
        id = 10

        self.messageDAO.deleteMessage(id)

        args = { 'chatname': 'Radahns Battlefield' }
    
        expected = self.data[8:4:-1]
        result = self.messageDAO.getMessages(args)

        self.assertEqual(expected, result)

    def testDeleteMessageFalseID(self):
        id = 999

        self.messageDAO.deleteMessage(id)

        args = { 'chatname': 'Radahns Battlefield' }
    
        expected = self.data[9:4:-1]
        result = self.messageDAO.getMessages(args)

        self.assertEqual(expected, result)

    def testEditMessage(self):
        message = Message({
            'id': 4,
            'message': 'Nah not with the club man',
            'edited': False,
            'timestamp': datetime(2012, 7, 17, 10, 3, 15),
            'username': 'Morgott',
            'chatname': 'Erdtree Sanctuary'
        })

        self.messageDAO.editMessage(message)

        args = { 'chatname': 'Erdtree Sanctuary' }
        expected = self.data[4::-1]
        expected[1] = (4, 'Nah not with the club man', True, datetime(2012, 7, 17, 10, 3, 15), 'Morgott', 'Erdtree Sanctuary')
        result = self.messageDAO.getMessages(args)

        self.assertEqual(expected, result)
