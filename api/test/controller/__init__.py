from __future__ import absolute_import
from controller import userController
from unittest import TestCase
from test.persistence.mockDAO import MockUserDAO
from fastapi import FastAPI
from fastapi.testclient import TestClient

userController.assignDAO(MockUserDAO())

app = FastAPI()
app.include_router(userController.router)

testClient = TestClient(app)

def testHttpRequest(test: TestCase, url: str, method: str, headers: dict, body: dict, expected_code: int = 200): 
    '''Helper function that sends a request, tests the outcome and returns the response data'''
    match (method):
        case 'GET':
            response = testClient.get(url, headers=headers)
        case 'POST':
            response = testClient.post(url, headers=headers, json=body)
        case 'PUT':
            response = testClient.put(url, headers=headers, json=body)
        case 'DELETE':
            response = testClient.delete(url, headers=headers)
        case _:
            raise ValueError
    test.assertEqual(expected_code, response.status_code)
    return response.json()