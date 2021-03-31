from flask import jsonify
from flask_restful import reqparse, abort, Resource
from . import db_session
from .couriers import Courier

parser = reqparse.RequestParser()
parser.add_argument('data', required=False, action='append') # для примера

parser_self_arguments = reqparse.RequestParser()
parser_self_arguments.add_argument('courier_type', required=False)
parser_self_arguments.add_argument('regions', required=False)
parser_self_arguments.add_argument('working_hours', required=False)



def abort_if_not_found(id):
        abort(404, message=f"courier {id} not found") # функция для вызова ошибки и возврата message


class CourierResource(Resource):
    def get(self, id):
        db_sess = db_session.create_session()
        user = db_sess.query(Courier).filter(Courier.courier_id == id).first()
        return jsonify(user.to_dict())# тут какая-то твоя работа функции которая возвращает json


    def patch(self, id):
        db_sess = db_session.create_session()
        user = db_sess.query(Courier).filter(Courier.courier_id == id).first()

        args = parser_self_arguments.parse_args()
        try:
            if args['courier_type']:
                user.courier_type = args['courier_type']
            if args['regions']:
                user.regions = args['regions']
            if args['working_hours']:
                user.working_hours = args['working_hours']

            db_sess.commit()
        except Exception:
            print(Exception.__class__.__name__)

        user = db_sess.query(Courier).filter(Courier.courier_id == id).first()

        return jsonify(user.to_dict())


class CouriersListResource(Resource):
    def post(self):
        db_sess = db_session.create_session()
        args = parser.parse_args()
        L = reqparse.request.json()
        if args['data']:  # пример обращения к аргументам парсера
            for elem in args['data']:
                L.append(elem)
                # courier = Courier()
                # courier.courier_id = elem['courier_id']
                # courier.courier_type = elem['courier_type']
                # courier.regions = elem['regions']
                # courier.working_hours = elem['working_hours']
                # db_sess.add(courier)
                # db_sess.commit()
        return jsonify(L)