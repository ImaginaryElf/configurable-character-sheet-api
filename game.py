from flask import request
from flask_cors import cross_origin
from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args

from mongo_repository import save_game, get_game


class GameApi(Resource):
    game_args = {
        "id": fields.Str(required=True)
    }

    @cross_origin()
    @use_args(game_args)
    def get(self, args):
        game = get_game(args['id'])
        return {'status': True, 'data': game}

    @cross_origin()
    def post(self):
        data = request.json
        game_id = save_game(data)
        return {'status': True, 'data': game_id}
