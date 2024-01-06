from __future__ import absolute_import
from fastapi import FastAPI, APIRouter, Request, Response, HTTPException
from persistence.DAO import UserDAO
from model.User import UserAuth

router = APIRouter()
auth = UserAuth()
def assignDAO(dao: UserDAO):
    auth.assignDAO(dao)

@router.get("/users", status_code=200)
async def get_users():
    # TODO: Session key validation
    return auth.getUsers()

@router.post("/login", status_code=200)
async def login(request: Request):
    body = await request.json()
    username = body['username']
    password = body['password']
    if (not auth.checkLogin(username, password)):
        raise HTTPException(status_code=403, detail='Password check failed')
    # TODO: Session key management

@router.post("/register", status_code=201)
async def register(request: Request):
    body = await request.json()
    username = body['username']
    password = body['password']
    auth.createUser(username, password)

@router.put("/login", status_code=200)
async def change_password(request: Request):
    # TODO: Session key validation
    headers = request.headers
    body = await request.json()
    username = headers['username']
    old_password = body['old_password']
    new_password = body['new_password']
    if (not auth.checkLogin(username, old_password)):
        raise HTTPException(status_code=403, detail='Password check failed')
    auth.setPassword(username, new_password)

@router.put("/users", status_code=200)
async def change_username(request: Request):
    # TODO: Session key validation
    headers = request.headers
    body = await request.json()
    old_username = headers['username']
    new_username = body['username']
    password = body['password']
    if (not auth.checkLogin(old_username, password)):
        raise HTTPException(status_code=403, detail='Password check failed')
    auth.setUsername(old_username, new_username)