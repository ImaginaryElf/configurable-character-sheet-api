from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin

from game import GameApi

app = Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


class HealthCheckApi(Resource):
    @cross_origin()
    def get(self):
        return {'status': True}


class HomeApi(Resource):
    @cross_origin()
    def get(self):
        return {'status': True}


api.add_resource(HealthCheckApi, '/health_check')
api.add_resource(HomeApi, '/')
api.add_resource(GameApi, '/game')

if __name__ == '__main__':
    app.run(port=5000)
