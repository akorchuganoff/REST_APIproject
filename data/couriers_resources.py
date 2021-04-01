from flask import jsonify, request, make_response
from flask_restful import reqparse, abort, Resource
from . import db_session
from .couriers import Courier
from .regions import Regions

parser = reqparse.RequestParser()
parser.add_argument('data', required=False, type=dict, action='append') # для примера

parser_self_arguments = reqparse.RequestParser()
parser_self_arguments.add_argument('courier_type', required=False)
parser_self_arguments.add_argument('regions', required=False, type=int, action='append')
parser_self_arguments.add_argument('working_hours', required=False)


def abort_if_not_found(id):
        abort(404, message=f"courier {id} not found")# функция для вызова ошибки и возврата message


class CourierResource(Resource):
    def get(self, id):
        db_sess = db_session.create_session()
        user = db_sess.query(Courier).filter(Courier.courier_id == id).first()
        reg = list(map(lambda region: region.region, user.regions))

        d = user.to_dict(only=("courier_id", "courier_type", "working_hours"))
        d['regions'] = reg
        return jsonify(d)# тут какая-то твоя работа функции которая возвращает json


    def patch(self, id):
        db_sess = db_session.create_session()
        user = db_sess.query(Courier).filter(Courier.courier_id == id).first()
        args = parser_self_arguments.parse_args()
        try:
            if args['courier_type']:
                user.courier_type = args['courier_type']
            if args['regions']:
                for i in range(1, len(user.regions)+1):
                    user.regions.remove(user.regions[0])
                db_sess.commit()

                for reg in args['regions']:
                    region = db_sess.query(Regions).filter(Regions.region == reg).first()
                    if not region:
                        region = Regions()
                        region.region = reg
                        db_sess.add(region)
                        db_sess.commit()

                    user.regions.append(region)
                    db_sess.commit()

            if args['working_hours']:
                user.working_hours = args['working_hours']
                db_sess.commit()
        except Exception:
            print(Exception.__class__.__name__)

        user = db_sess.query(Courier).filter(Courier.courier_id == id).first()
        reg = list(map(lambda regions: regions.region, user.regions))
        d = user.to_dict(only=("courier_id", "courier_type", "working_hours"))
        d['regions'] = reg
        return jsonify(d)


class CouriersListResource(Resource):
    def post(self):
        # db_sess = db_session.create_session()
        args = parser.parse_args()

        valid = []
        invalid = []

        for elem in args['data']:
            db_sess = db_session.create_session()
            # try:
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
            db_sess.add(courier)
            db_sess.commit()

            courier = db_sess.query(Courier).filter(Courier.courier_id == elem['courier_id']).first()

            for reg in elem['regions']:
                region = db_sess.query(Regions).filter(Regions.region == reg).first()
                if not region:
                    region = Regions()
                    region.region = reg
                    db_sess.add(region)
                    db_sess.commit()

                courier.regions.append(region)
                db_sess.commit()
            valid.append({'id': elem['courier_id']})
        #     except Exception:
        #         # return {'id': elem['courier_id']}
        #         invalid.append({'id': elem['courier_id']})
        #
        # if len(invalid) != 0:
        #     data = {"message": "Bad Request", "validation_error": {"couriers": invalid}}
        #     return make_response(jsonify(data), 400)

        data = {"message": "Created", "couriers": valid}
        return make_response(jsonify(data), 201)