from dotenv import load_dotenv
load_dotenv()
from fastapi import Depends, FastAPI
from pydantic import BaseModel
import uvicorn
from model.dbcredential import DBCredential
import model
from model.apimodel import APIModel
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from repository.database import SessionLocal, engine
from routers.private import user, api
from routers.public import login, user as user_public, healthcheck
import os
import json

internal_user = os.environ['INTERNAL_DB_USER']
internal_host = os.environ['INTERNAL_DB_HOST']


app = FastAPI()
app.include_router(healthcheck.router)
app.include_router(api.router)
app.include_router(login.router)
app.include_router(user_public.router)
app.include_router(user.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.get("/", include_in_schema=False)
async def main():
    return RedirectResponse(url="/docs/")

if __name__ == '__main__':
    try:
        model.dbcredential.Base.metadata.create_all(bind=engine)
        print(f"Connection to the {internal_host} for user {internal_user} created successfully.")
        uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
    except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)