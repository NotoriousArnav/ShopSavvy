__import__("dotenv").load_dotenv() #Dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import routers
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
async def root():
    """API Endpoint to Check if Server is Up"""
    return {"message": "Hello World"}

for router in routers: app.include_router(router)
