from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://Babaq:3bJjvdRy8zzGivwI@youngjourney.e8m4u.mongodb.net/?retryWrites=true&w=majority&appName=YoungJourney"

client = MongoClient(uri, server_api=ServerApi('1'))

collection_users = client.Users.Users

try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB")
except Exception as e:
    print("Failed to connect to MongoDB")


# db.py
from pymongo import MongoClient

def get_database():
    # Подключение к MongoDB
    client = MongoClient("mongodb://localhost:27017")
    return client["my_database"]

def add_user(user_data):
    db = get_database()
    db.users.insert_one(user_data)
    print("User added successfully")

def find_user(user_id):
    db = get_database()
    return db.users.find_one({"_id": user_id})