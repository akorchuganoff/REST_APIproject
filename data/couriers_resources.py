from flask import jsonify, make_response
from flask_restful import reqparse, abort, Resource
from . import db_session
from .couriers import Courier
from .regions import CourierToRegion, Regions
from .orders import CourierToOrder, Orders
from.order_resources import check_time

parser = reqparse.RequestParser()
parser.add_argument('data', required=False, type=dict, action='append')

parser_self_arguments = reqparse.RequestParser()
parser_self_arguments.add_argument('courier_type', required=False)
parser_self_arguments.add_argument('regions', required=False, type=int, action='append')
parser_self_arguments.add_argument('working_hours', required=False)


class CourierResource(Resource):
    # noinspection PyMethodMayBeStatic
    def get(self, id):
        db_sess = db_session.create_session()
        courier = db_sess.query(Courier).filter(Courier.courier_id == id).first()

        courier_to_region = db_sess.query(CourierToRegion).filter(CourierToRegion.courier_id == id).all()
        reg = list(map(lambda regions: regions.region_id, courier_to_region))
        d = courier.to_dict(only=("courier_id", "courier_type", "working_hours", "rating", "earnings"))
        d['regions'] = reg
        return jsonify(d)

    # noinspection PyMethodMayBeStatic
    def patch(self, id):
        db_sess = db_session.create_session()
        courier = db_sess.query(Courier).filter(Courier.courier_id == id).first()
        args = parser_self_arguments.parse_args()
        # noinspection PyBroadException
        try:
            if args['courier_type']:
                courier.courier_type = args['courier_type']
            if args['regions']:
                db_sess.query(CourierToRegion).filter(CourierToRegion.courier_id == courier.courier_id).delete()
                db_sess.commit()

                for reg in args['regions']:
                    region = db_sess.query(Regions).filter(Regions.region == reg).first()
                    if not region:
                        region = Regions()
                        region.region = reg
                        db_sess.add(region)
                        db_sess.commit()

                    courier_to_region = CourierToRegion()
                    courier_to_region.courier = courier
                    courier_to_region.region = region
                    db_sess.add(courier_to_region)
                    db_sess.commit()

            if args['working_hours']:
                courier.working_hours = args['working_hours']
                db_sess.commit()

            orders = db_sess.query(Orders).filter(Orders.flag == 'assigned', Orders.region.notin_(args['regions']))
            for order in orders:
                courier_to_order = db_sess.query(CourierToOrder).filter(
                    CourierToOrder.courier_id == courier.courier_id,
                    CourierToOrder.order_id == order.order_id).first()
                if not courier_to_order:
                    continue
                order.flag = None
                courier.weight_of_food -= order.weight
                db_sess.delete(courier_to_order)
                db_sess.commit()

            courier_to_order = db_sess.query(CourierToOrder).filter(
                CourierToOrder.courier_id == courier.courier_id).all()

            for c_to_o in courier_to_order:
                order = db_sess.query(Orders).filter(Orders.order_id == c_to_o.order_id).first()
                if not check_time(courier, order):
                    order.flag = None
                    courier.weight_of_food -= order.weight
                    db_sess.delete(courier_to_order)
                    db_sess.commit()

            arr_courier_to_order = db_sess.query(CourierToOrder).filter(
                CourierToOrder.courier_id == courier.courier_id).all()
            i = 0
            while courier.max_weight < courier.weight_of_food:
                c_to_o = arr_courier_to_order[i]
                order = db_sess.query(Orders).filter(Orders.order_id == c_to_o.order_id).first()
                order.flag = None
                courier.weight_of_food -= order.weight
                db_sess.delete(c_to_o)
                db_sess.commit()
                i += 1
        except Exception:
            print(Exception.__class__.__name__)

        courier_to_region = db_sess.query(CourierToRegion).filter(CourierToRegion.courier_id == id).all()
        reg = list(map(lambda regions: regions.region_id, courier_to_region))
        d = courier.to_dict(only=("courier_id", "courier_type", "working_hours"))
        d['regions'] = reg
        return jsonify(d)


class CouriersListResource(Resource):
    # noinspection PyMethodMayBeStatic
    def post(self):
        db_sess = db_session.create_session()
        args = {}
        # noinspection PyBroadException
        try:
            args = parser.parse_args()
        except BaseException:
            abort(400, message='Bad request')

        valid = []
        invalid = []
        for elem in args['data']:
            try:
                if type(elem['courier_id']) == int and type(elem['courier_type']) == str and type(
                        elem['working_hours']) == list and type(elem['regions']) == list:
                    if elem['courier_id'] in list(map(lambda c: c.courier_id, db_sess.query(Courier).all())):
                        raise Exception

                    for t in elem['working_hours']:
                        if type(t) != str:
                            raise Exception

                    for r in elem['regions']:
                        if type(r) != int:
                            raise Exception

                    continue
                else:
                    raise Exception
            except Exception:
                invalid.append({'id': elem['courier_id']})

        if len(invalid) != 0:
            data = {"message": "Bad Request", "validation_error": {"couriers": invalid}}
            return make_response(jsonify(data), 400)

        for elem in args['data']:
            # noinspection PyBroadException
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

            for reg in elem['regions']:
                region = db_sess.query(Regions).filter(Regions.region == reg).first()
                if not region:
                    region = Regions()
                    region.region = reg
                    db_sess.add(region)

                courier_to_region = CourierToRegion()
                courier_to_region.courier = courier
                courier_to_region.region = region
                db_sess.add(courier_to_region)
            valid.append({'id': elem['courier_id']})
            # except Exception:
            #     invalid.append({'id': elem['courier_id']})

        db_sess.commit()
        data = {"message": "Created", "couriers": valid}
        return make_response(jsonify(data), 201)
