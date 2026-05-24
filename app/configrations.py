# configrations.py

from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://minji_db_user:<db_password>@galpi.qqwnswr.mongodb.net/?appName=galpi?retryWrites=true&w=majority&tls=true"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.galpi
collection = db["galpi_data"]