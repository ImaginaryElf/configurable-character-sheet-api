from pymongo import MongoClient
from pymongo.server_api import ServerApi

conn_str = "mongodb+srv://admin:BZiJZjt6Fhqt9Isq@project-cluster.9imd1.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(conn_str, serverSelectionTimeoutMS=5000, server_api=ServerApi('1'))
gameCollection = client["public"]["game"]


def create_game(game):
    result = gameCollection.insert_one(game)
    return result.inserted_id


def update_game(game):
    result = gameCollection.replace_one({'_id': game['_id']}, game)
    return result.acknowledged


def get_game(game_id):
    result = gameCollection.find_one({'_id': game_id})
    return result


def get_games_by_player(player_id):
    # player in players where player._id == player_id
    return gameCollection.find({'players': {"$elemMatch": {"player_id": player_id}}})


def get_games_by_gm(gm_id):
    return gameCollection.find({'gm_id': gm_id})


def get_game_by_character(character_id):
    # player in players where player._id == player_id
    return gameCollection.find_one(
        {'players':
             {"$elemMatch":
                  {"characters":
                       {"$elemMatch":
                            {"character_id": character_id}
                        }
                   }
              }
         })
