from flask import jsonify, request
from flask_restful import reqparse, abort, Resource
from . import db_session
from .couriers import Courier
from .regions import Regions

parser = reqparse.RequestParser()
parser.add_argument('data', required=False, type=dict, action='append') # для примера

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
        L = []
        for elem in args['data']:
            courier = Courier()
            courier.courier_id = elem['courier_id']
            courier.courier_type = elem['courier_type']

            courier.working_hours = ' '.join(map(str, elem['working_hours']))

            if courier.courier_type == 'foot':
                courier.max_weight = 10
            elif courier.courier_type == 'bike':
                courier.max_weight = 20
            else:
                courier.max_weight = 50


            # courier.regions = [Regions(region=elem['regions'][0]), Regions(region=elem['regions'][1])]

            db_sess.add(courier)
            db_sess.commit()

            for reg in elem['regions']:
                region = Regions()
                region.courier = courier
                region.region = reg
                # courier.regions.append(region)
                db_sess.add(region)
                db_sess.commit()


            user = db_sess.query(Courier).filter(Courier.courier_id == elem['courier_id']).first()
            # L.append(user.regions) # Переназвать нормально
            L=[]

        return jsonify(L)