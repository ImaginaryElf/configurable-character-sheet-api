from pymongo import MongoClient
from pymongo.server_api import ServerApi

conn_str = "mongodb+srv://admin:<password>@project-cluster.9imd1.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(conn_str, serverSelectionTimeoutMS=5000, server_api=ServerApi('1'))
gameDb = client.game
layoutDb = client.layout
characterDb = client.character
userDb = client.user


def save_game(game_schema_json):
    result = gameDb.insert_one(game_schema_json)
    return result.inserted_id


def get_game(game_id):
    result = gameDb.find_one({'_id': game_id})
    return result
