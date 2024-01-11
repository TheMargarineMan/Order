from __future__ import absolute_import
from fastapi import FastAPI, APIRouter, Request, HTTPException
from model.Message import Message
from persistence.DAO import MessageDAO

router = APIRouter()
dataObject = None

def assignDAO(dao: MessageDAO):
    global dataObject
    dataObject = dao 

@router.get('/', status_code=200)
async def getMessages(chatname: str, request: Request):
    # TODO: Permissions and Authentication
    args = request.headers
    return dataObject.getMessages(chatname, args)

@router.post('/', status_code=201)
async def createMessage(chatname: str, request: Request):
    message = Message(await request.json())
    return dataObject.createMessage(chatname, message)

@router.put('/', status_code=200)
async def editMessage(chatname: str, request: Request):
    message = Message(await request.json())
    dataObject.editMessage(chatname, message)

@router.delete('/{msg_id}', status_code=200)
async def deleteMessage(chatname: str, msg_id: int):
    dataObject.deleteMessage(chatname, msg_id)
