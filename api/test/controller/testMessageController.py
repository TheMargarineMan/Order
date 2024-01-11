from __future__ import absolute_import
from .__init__ import messageController, testHttpRequest
from unittest import TestCase
from datetime import datetime
from fastapi import HTTPException
from fastapi.testclient import TestClient
from test.persistence.mockDAO import MockMessageDAO

class TestMessageController(TestCase):
    data = [
        [1, 'Fools emboldened by the flame of ambition.', False, '2012-07-17T10:00:00', 'Morgott'],
        [2, 'My brother in Marika you wear rags and you call yourself "King".', False, '2012-07-17T10:00:10', 'Tarnished'],
        [3, '*Bodies Morgott*', False, '2012-07-17T10:03:00', 'Tarnished'],
        [4, 'Literally how. Nah he hacking get him out.', False, '2012-07-17T10:03:15', 'Morgott'],
        [5, 'L Bozo + mad + skill issue + golden order fell off + go back to the sewers', False, '2012-07-17T10:03:20', 'Tarnished'],
        [6, 'GRARARRHRHHRHHR', False, '2012-07-23T13:00:00', 'Radahn'],
        [7, 'Bro why is he growling. Ur not him', False, '2012-07-23T13:00:05', 'Tarnished'],
        [8, 'GUH!!!', False, '2012-07-23T13:02:12', 'Radahn'],
        [9, '*Bodies Radahn*', False, '2012-07-23T13:05:32', 'Tarnished'],
        [10, 'Imagine learning gravity magic just to be beat by a guy with a stick.', False, '2012-07-23T13:05:45', 'Tarnished']
    ]

    maxDiff = None

    def setUp(self):
        messageController.assignDAO(MockMessageDAO())

    def testGetMessagesChatOne(self):
        chatname = 'Erdtree Sanctuary'

        expected = self.data[4::-1]
        result = testHttpRequest(self, f'/chat/{chatname}', 'GET', {}, {})
        self.assertEqual(expected, result)
        
    def testGetMessagesChatTwo(self):
        chatname = 'Grand Study Hall'

        result = testHttpRequest(self, f'/chat/{chatname}', 'GET', {}, {})

        self.assertTrue(len(result) == 0)

    def testGetMessagesChatThree(self):
        chatname = 'Radahns Battlefield'

        expected = self.data[:4:-1]
        result = testHttpRequest(self, f'/chat/{chatname}', 'GET', {}, {})

        self.assertEqual(expected, result)

    def testGetMessageContains(self):
        chatname = 'Erdtree Sanctuary'
        args = { 'contains': 'f' }
        
        expected = [self.data[4], self.data[1], self.data[0]]
        result = testHttpRequest(self, f'/chat/{chatname}', 'GET', args, {})

        self.assertEqual(expected, result)

    def testGetMessageUser(self):
        chatname = 'Erdtree Sanctuary'
        args = { 'username': 'Morgott' }
        
        expected = [self.data[3], self.data[0]]
        result = testHttpRequest(self, f'/chat/{chatname}', 'GET', args, {})
    
        self.assertEqual(expected, result)

    def testGetMessageBefore(self):
        chatname = 'Erdtree Sanctuary'
        args = { 'before': '2012-7-17T10:03:10' }
        
        expected = self.data[2::-1]
        result = testHttpRequest(self, f'/chat/{chatname}', 'GET', args, {})
    
        self.assertEqual(expected, result)

    def testGetMessageAfter(self):
        chatname = 'Erdtree Sanctuary'
        args = { 'after': '2012-7-17T10:03:10' }
        
        expected = self.data[4:2:-1]
        result = testHttpRequest(self, f'/chat/{chatname}', 'GET', args, {})
    
        self.assertEqual(expected, result)

    def testGetMessageGarbageArgument(self):
        chatname = 'Erdtree Sanctuary'
        args = { 'garbage': 'garbage' }

        expected = self.data[4::-1]
        result = testHttpRequest(self, f'/chat/{chatname}', 'GET', args, {})

        self.assertEqual(expected, result)

    def testCreateMessage(self):
        chatname = 'Grand Study Hall'
        message = {
            "message": "Shadow Wizard Money Gang",
            "edited": False,
            "timestamp": '2012-07-18T10:00:00',
            "username": "Melina"
        }

        # Test if returned id was as expected        
        result = testHttpRequest(self, f'/chat/{chatname}', 'POST', {}, message, 201)
        expected = 11
        
        self.assertEqual(expected, result)

        # Test existence in chatroom            
        expected = [[11, "Shadow Wizard Money Gang", False, '2012-07-18T10:00:00', "Melina"]]
        result = testHttpRequest(self, f'/chat/{chatname}', 'GET', {}, {})

        self.assertEqual(expected, result)

    def testDeleteMessage(self):
        chatname = 'Radahns Battlefield'
        msg_id = 10

        testHttpRequest(self, f'/chat/{chatname}/{msg_id}', 'DELETE', {}, {})
    
        expected = self.data[8:4:-1]
        result = testHttpRequest(self, f'/chat/{chatname}', 'GET', {}, {})

        self.assertEqual(expected, result)

    def testDeleteMessageFalseID(self):
        chatname = 'Radahns Battlefield'
        msg_id = 999

        testHttpRequest(self, f'/chat/{chatname}/{msg_id}', 'DELETE', {}, {})
    
        expected = self.data[9:4:-1]
        result = testHttpRequest(self, f'/chat/{chatname}', 'GET', {}, {})

        self.assertEqual(expected, result)

    def testEditMessage(self):
        chatname = 'Erdtree Sanctuary'
        message = {
            'id': 4,
            'message': 'Nah not with the club man',
            'edited': False,
            'timestamp': '2012-07-17T10:03:15',
            'username': 'Morgott'
        }

        result = testHttpRequest(self, f'/chat/{chatname}', 'PUT', {}, message)

        expected = self.data[4::-1]
        expected[1] = [4, 'Nah not with the club man', True, '2012-07-17T10:03:15', 'Morgott']
        result = testHttpRequest(self, f'/chat/{chatname}', 'GET', {}, {})

        self.assertEqual(expected, result)