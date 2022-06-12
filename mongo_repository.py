from pymongo import MongoClient
from pymongo.server_api import ServerApi

conn_str = "mongodb+srv://admin:<password>@project-cluster.9imd1.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(conn_str, serverSelectionTimeoutMS=5000, server_api=ServerApi('1'))
db = client.test
