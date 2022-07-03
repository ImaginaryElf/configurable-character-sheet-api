from flask import request
from flask_cors import cross_origin
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args

from mongo_repository import get_game, update_game


class PlayerApi(Resource):

    @cross_origin()
    def post(self):
        data = request.json
        game_id = data['game_id']
        player = { "player_id": data['player_id'], "characters": [] }
        game = get_game(game_id)
        if game is None:
            return {'status': False, 'error': 'Game not found'}
        game['players'].append(player)
        result = update_game(game)
        if result is True:
            return {'status': True, 'data': game_id}
        else:
            return {'status': False, 'error': 'Game failed to update'}
