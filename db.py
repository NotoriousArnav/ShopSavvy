__import__("dotenv").load_dotenv() #Dotenv
import os

# We will use Mongo DB for Horizontal scaling
from pymongo import MongoClient
client = MongoClient(os.environ.get("MONGO_URI"))


db = client['shop']

users = db['users']
products = db['products']

