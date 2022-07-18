from flask import request
from flask_cors import cross_origin
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
from uuid import uuid4

from mongo_repository import get_game_by_character, get_game, update_game


class CharacterApi(Resource):
    character_args = {
        "character_id": fields.Str(),
        "player_id": fields.Str(),
        "game_id": fields.Str()
    }

    @cross_origin()
    @use_args(character_args, location="query")
    def get(self, args):
        characters = []
        if 'character_id' in args:
            game = get_game_by_character(args['character_id'])
            if game is not None:
                for player in game['players']:
                    for character in player['characters']:
                        if character['character_id'] == args['character_id']:
                            characters.append(character)
                            return {'status': True, 'data': characters}
            return {'status': False, 'error': 'Could not find character_id=' + args['character_id']}

        if 'game_id' in args:
            game = get_game(args['game_id'])
            if game is not None:
                if args['player_id'] is not None:
                    for player in game['players']:
                        if player['player_id'] == args['player_id']:
                            return {'status': True, 'data': player['characters']}
                    return {'status': False, 'error': 'Game with _id=' + args['game_id'] +
                                                      " contained not player with player_id=" + args['player_id']}
                else:
                    for player in game['players']:
                        characters.extend(player['characters'])
                    return {'status': True, 'data': characters}
            return {'status': False, 'error': 'Could not find game with _id=' + args['game_id']}

        if 'player_id' in args:
            games = get_game_by_character(args['player_id'])
            for game in games:
                for player in game['players']:
                    if player['player_id'] == args['player_id']:
                        characters.append(player['characters'])
            return {'status': False, 'data': characters}

        return {'status': False, 'error': 'You must provide at least one of character_id, player_id, or game_id'}

    @cross_origin()
    def post(self):
        data = request.json
        game = get_game(data['game_id'])
        if game is None:
            return {'status': False, 'error': 'Game not found'}
        for player in game['players']:
            if player['player_id'] == data['player_id']:
                character = {'character_id': str(uuid4()), 'data': data['character_data']}
                player['characters'].append(character)
                result = update_game(game)
                if result is True:
                    return {'status': True, 'data': character}
                else:
                    return {'status': False, 'error': 'Update failed'}
        return {'status': False, 'error': 'Player not found in game'}

    @cross_origin()
    def put(self):
        data = request.json
        game = get_game(data['game_id'])
        if game is None:
            return {'status': False, 'error': 'Game not found'}
        for player in game['players']:
            if player['player_id'] == data['player_id']:
                for character in player['characters']:
                    if character['character_id'] == data['character']['character_id']:
                        character['data'] = data['character']['data']
                        result = update_game(game)
                        if result is True:
                            return {'status': True}
                        else:
                            return {'status': False, 'error': 'Update failed'}
                return {'status': False, 'error': 'Character not found in player'}
        return {'status': False, 'error': 'Player not found in game'}
