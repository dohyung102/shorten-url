from fastapi import FastAPI, Depends
from sqlmodel import SQLModel

from database import engine, get_session
from router import shotyUrlRouter


app = FastAPI(dependencies=[Depends(get_session)])

SQLModel.metadata.create_all(engine)

app.include_router(shotyUrlRouter.router)