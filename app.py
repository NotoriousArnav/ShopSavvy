__import__("dotenv").load_dotenv() #Dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import routers
from schemas.currency import default_currency
import os

app = FastAPI(
    title=os.getenv("STORE_NAME", "ShopSavvy"),
    version="alpha",
    description=f"""A software solution for store management.
        Default Currency is set to {default_currency.name} ({default_currency.symbol})""",
)

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
