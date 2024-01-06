from fastapi import FastAPI
from controller import userController
from persistence.postgres.userDAO import PostgresUserDAO

userController.init(PostgresUserDAO())

app = FastAPI()
app.include_router(userController.router, prefix='/user')

@app.get("/")
async def root():
    return {"message": "Hello World"}
