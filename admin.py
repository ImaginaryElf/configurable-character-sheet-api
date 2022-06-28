from flask_cors import cross_origin
from flask_restful import Resource


class AdminApi(Resource):
    @cross_origin()
    def post(self):
        return {'status': True}
