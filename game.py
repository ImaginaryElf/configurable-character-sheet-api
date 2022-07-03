from flask import request
from flask_cors import cross_origin
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args

from mongo_repository import create_game, update_game, get_game
from mongo_repository import get_game_by_character, get_games_by_gm, get_games_by_player


class GameApi(Resource):
    game_args = {
        "game_id": fields.Str(),
        "character_id": fields.Str(),
        "player_id": fields.Str(),
        "gm_id": fields.Str()
    }

    @cross_origin()
    @use_args(game_args)
    def get(self, args):
        games = []
        if args['game_id'] is not None:
            game = get_game(args['id'])
            if game is not None:
                games.append(game)
                return {'status': True, 'data': games}
            else:
                return {'status': False, 'error': 'Game not found'}

        if args['character_id'] is not None:
            game = get_game_by_character(args['character_id'])
            if game is not None:
                games.append(game)
                return {'status': True, 'data': games}
            else:
                return {'status': False, 'error': 'Game not found'}

        if args['gm_id'] is not None:
            potential_games = get_games_by_gm(args['gm_id'])
            for game in potential_games:
                if args['player_id'] is None:
                    games.append(game)
                else:
                    for player in game['players']:
                        if player['player_id'] == args['player_id']:
                            games.append(game)
            return {'status': True, 'data': games}

        if args['player_id'] is not None:
            games = get_games_by_player(args['player_id'])
            return {'status': True, 'data': games}

        return {'status': False, 'error': 'You must provide at least one of character_id, player_id, game_id, or gm_id'}

    @cross_origin()
    def post(self):
        data = request.json
        if data['name'] is not None and data['schema'] is not None and data['layout'] is not None and data['gm_id'] is not None:
            game_id = create_game(data)
            return {'status': True, 'data': game_id}
        else:
            return {'status': False, 'error': 'Game must contain name, schema, layout, and gm_id'}

    @cross_origin()
    def put(self):
        data = request.json
        game = get_game(data['id'])
        if game is None:
            return {'status': False, 'error': 'Game not found'}
        game['name'] = data['name']
        result = update_game(game)
        return {'status': result}
