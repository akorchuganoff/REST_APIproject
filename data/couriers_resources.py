from flask import jsonify
from flask_restful import reqparse, abort, Resource
from . import db_session
from .couriers import Courier

parser = reqparse.RequestParser()
parser.add_argument('id', required=False, type=int)
parser.add_argument('data', required=False, action='append') # для примера

db_sess = db_session.create_session()

def abort_if_not_found(id):
        abort(404, message=f"courier {id} not found") # функция для вызова ошибки и возврата message


class CourierResource(Resource):
    def get(self, id):
        user = db_sess.query(Courier).filter(Courier.courier_id == id)
        return jsonify(user)# тут какая-то твоя работа функции которая возвращает json

    def delete(self, id):
        return jsonify({'success': 'OK'}) # на удаление примитив ok

    def patch(self, id):
        return jsonify({'success': 'OK'})  # на удаление примитив ok


class CouriersListResource(Resource):
    def get(self):
        return jsonify({'success': 'OK'})# тут какая-то твоя работа функции которая возвращает json

    def post(self):
        args = parser.parse_args()
        L = []
        if args['data']:  # пример обращения к аргументам парсера
            for elem in args['data']:
                L.append(elem)
        return jsonify(L)