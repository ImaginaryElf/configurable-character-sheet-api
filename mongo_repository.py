import json

from bson import json_util, ObjectId
from pymongo import MongoClient
from pymongo.server_api import ServerApi

conn_str = "mongodb+srv://admin:BZiJZjt6Fhqt9Isq@project-cluster.9imd1.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(conn_str, serverSelectionTimeoutMS=5000, server_api=ServerApi('1'))
gameCollection = client["public"]["game"]


def create_game(game):
    result = gameCollection.insert_one(game)
    return json.loads(json_util.dumps(result.inserted_id))


def update_game(game):
    result = gameCollection.replace_one({'_id': ObjectId(game['_id'])}, game)
    return json.loads(json_util.dumps(result.acknowledged))


def get_game(game_id):
    result = gameCollection.find_one({'_id': ObjectId(game_id)})
    return json.loads(json_util.dumps(result))


def get_games_by_player(player_id):
    # player in players where player._id == player_id
    result = gameCollection.find({'players': {"$elemMatch": {"id": player_id}}})
    return json.loads(json_util.dumps(result))


def get_games_by_gm(gm_id):
    result = gameCollection.find({'gm_id': gm_id})
    return json.loads(json_util.dumps(result))


def get_game_by_character(character_id):
    # player in players where player._id == player_id
    result = gameCollection.find_one(
        {'players':
             {"$elemMatch":
                  {"characters":
                       {"$elemMatch":
                            {"id": character_id}
                        }
                   }
              }
         })
    return json.loads(json_util.dumps(result))
