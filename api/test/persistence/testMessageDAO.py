from __future__ import absolute_import
from unittest import TestCase
from datetime import datetime
from model.Message import Message
from test.persistence.mockDAO import MockMessageDAO

class TestMessageDAO(TestCase):
    """
    This test class is for the testing of implementations of MessageDAO.
    This test class by default tests the MockMessageDAO implementation.
    This test class can be inherited in order to perform tests on other
    implementations of MessageDAO, as long as the setUp(), setUpClass() 
    and tearDownClass() methods are properly defined in the child tester.
    """

    data = [
        (1, 'Fools emboldened by the flame of ambition.', False, datetime(2012, 7, 17 ,10, 0, 0), 'Morgott'),
        (2, 'My brother in Marika you wear rags and you call yourself "King".', False, datetime(2012, 7, 17, 10, 0, 10), 'Tarnished'),
        (3, '*Bodies Morgott*', False, datetime(2012, 7, 17, 10, 3, 0), 'Tarnished'),
        (4, 'Literally how. Nah he hacking get him out.', False, datetime(2012, 7, 17, 10, 3, 15), 'Morgott'),
        (5, 'L Bozo + mad + skill issue + golden order fell off + go back to the sewers', False, datetime(2012, 7, 17, 10, 3, 20), 'Tarnished'),
        (6, 'GRARARRHRHHRHHR', False, datetime(2012, 7, 23, 13, 0, 0), 'Radahn'),
        (7, 'Bro why is he growling. Ur not him', False, datetime(2012, 7, 23, 13, 0, 5), 'Tarnished'),
        (8, 'GUH!!!', False, datetime(2012, 7, 23, 13, 2, 12), 'Radahn'),
        (9, '*Bodies Radahn*', False, datetime(2012, 7, 23, 13, 5, 32), 'Tarnished'),
        (10, 'Imagine learning gravity magic just to be beat by a guy with a stick.', False, datetime(2012, 7, 23, 13, 5, 45), 'Tarnished')
    ]

    def setUp(self):
        self.messageDAO = MockMessageDAO()

    def testGetMessagesChatOne(self):
        chatname = 'Erdtree Sanctuary'

        expected = self.data[4::-1]
        result = self.messageDAO.getMessages(chatname)

        self.assertEqual(expected, result)

    def testGetMessagesChatTwo(self):
        chatname = 'Grand Study Hall'

        result = self.messageDAO.getMessages(chatname)

        self.assertTrue(len(result) == 0)

    def testGetMessagesChatThree(self):
        chatname = 'Radahns Battlefield'

        expected = self.data[:4:-1]
        result = self.messageDAO.getMessages(chatname)

        self.assertEqual(expected, result)

    def testGetMessageContains(self):
        chatname = 'Erdtree Sanctuary'
        args = { 'contains': 'f' }
        
        expected = [self.data[4], self.data[1], self.data[0]]
        result = self.messageDAO.getMessages(chatname, args)

        self.assertEqual(expected, result)

    def testGetMessageUser(self):
        chatname = 'Erdtree Sanctuary'
        args = { 'username': 'Morgott' }
        
        expected = [self.data[3], self.data[0]]
        result = self.messageDAO.getMessages(chatname, args)
    
        self.assertEqual(expected, result)

    def testGetMessageBefore(self):
        chatname = 'Erdtree Sanctuary'
        args = { 'before': '2012-7-17 10:03:10' }
        
        expected = self.data[2::-1]
        result = self.messageDAO.getMessages(chatname, args)
    
        self.assertEqual(expected, result)

    def testGetMessageAfter(self):
        chatname = 'Erdtree Sanctuary'
        args = { 'after': '2012-7-17 10:03:10' }
        
        expected = self.data[4:2:-1]
        result = self.messageDAO.getMessages(chatname, args)
    
        self.assertEqual(expected, result)

    def testGetMessageGarbageArgument(self):
        chatname = 'Erdtree Sanctuary'
        args = { 'garbage': 'garbage' }

        expected = self.data[4::-1]
        result = self.messageDAO.getMessages(chatname, args)

        self.assertEqual(expected, result)

    def testCreateMessage(self):
        chatname = 'Grand Study Hall'
        message = Message({
            "message": "Shadow Wizard Money Gang",
            "edited": False,
            "timestamp": '2012-7-18 10:0:0',
            "username": "Melina"
        })

        # Test if returned id was as expected        
        result = self.messageDAO.createMessage(chatname, message)
        expected = 11
        
        self.assertEqual(expected, result)

        # Test existence in chatroom            
        expected = [(11, "Shadow Wizard Money Gang", False, datetime(2012, 7, 18, 10, 0, 0), "Melina")]
        result = self.messageDAO.getMessages(chatname)

        self.assertEqual(expected, result)

    def testDeleteMessage(self):
        chatname = 'Radahns Battlefield'
        id = 10

        self.messageDAO.deleteMessage(chatname, id)
    
        expected = self.data[8:4:-1]
        result = self.messageDAO.getMessages(chatname)

        self.assertEqual(expected, result)

    def testDeleteMessageFalseID(self):
        chatname = 'Radahns Battlefield'
        id = 999

        self.messageDAO.deleteMessage(chatname, id)
    
        expected = self.data[9:4:-1]
        result = self.messageDAO.getMessages(chatname)

        self.assertEqual(expected, result)

    def testEditMessage(self):
        chatname = 'Erdtree Sanctuary'
        message = Message({
            'id': 4,
            'message': 'Nah not with the club man',
            'edited': False,
            'timestamp': datetime(2012, 7, 17, 10, 3, 15),
            'username': 'Morgott'
        })

        self.messageDAO.editMessage(chatname, message)

        expected = self.data[4::-1]
        expected[1] = (4, 'Nah not with the club man', True, datetime(2012, 7, 17, 10, 3, 15), 'Morgott')
        result = self.messageDAO.getMessages(chatname)

        self.assertEqual(expected, result)
