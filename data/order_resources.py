from flask import jsonify, request, make_response
from flask_restful import reqparse, abort, Resource
from . import db_session
from .orders import Orders
from .couriers import Courier
from .regions import Regions, CourierToRegion
from .orders import CourierToOrder
import datetime
import arrow

parser = reqparse.RequestParser()
parser.add_argument('data', required=False, type=dict, action='append')

assign_parser = reqparse.RequestParser()
assign_parser.add_argument('courier_id', required=True, type=int)

complete_parser = reqparse.RequestParser()
complete_parser.add_argument("courier_id", required=True, type=int)
complete_parser.add_argument("order_id", required=True, type=int)
complete_parser.add_argument("complete_time", required=True, type=str)

def checkTime(courier, order):
    times1 = courier.working_hours.split(' ')
    times2 = order.delivery_hours.split(' ')

    for t1 in times1:
        for t2 in times2:
            startb, endb = t2.split('-')
            sb = int(startb.split(':')[1]) + int(startb.split(':')[0]) * 60
            eb = int(endb.split(':')[0]) * 60 + int(endb.split(':')[1])

            starta, enda = t1.split('-')
            sa = int(starta.split(':')[0])*60 + int(starta.split(':')[1])
            ea = int(enda.split(':')[0]) * 60 + int(enda.split(':')[1])
            # print(order.order_id, sa, ea, sb, eb)
            if sa <= eb and ea >= sb:
                return True
    return False

class OrderListResource(Resource):
    def post(self):
        db_sess = db_session.create_session()
        args = parser.parse_args()
        valid = []
        invalid = []
        for elem in args['data']:
            try:
                db_sess = db_session.create_session()
                order = Orders()
                order.order_id = elem['order_id']
                order.weight = elem['weight']
                order.region = elem['region']
                order.delivery_hours = elem['delivery_hours']

                db_sess.add(order)
                db_sess.commit()

                order_get = db_sess.query(Orders).filter(Orders.order_id == elem['order_id']).first()
                valid.append({'id': order_get.order_id})
            except:
                invalid.append(elem['order_id'])

        if len(invalid) != 0:
            data = {'message': 'Bad request', "validation_error": {"orders": invalid}}
            return make_response(jsonify(data), 400)
        data = {'message': 'Created', "orders": valid}
        return make_response(jsonify(data), 201)


class OrderAssign(Resource):
    def post(self):
        db_sess = db_session.create_session()
        args = assign_parser.parse_args()
        id = args['courier_id']
        L = []
        courier = db_sess.query(Courier).filter(Courier.courier_id == id).first()
        if not courier:
            abort(400, message='Bad Request')
        reg = list(map(lambda region: region.region_id, courier.regions))
        print(reg)
        ans = []
        time = datetime.datetime.now(datetime.timezone.utc)
        for order in db_sess.query(Orders).all():
            if order.region in reg and order.weight < courier.max_weight - courier.weight_of_food and order.flag == None and checkTime(courier, order):
                print(order.order_id)

                courier_order = CourierToOrder()
                courier_order.courier = courier
                courier_order.order = order

                courier_order.assigned_time = time

                order.flag = 'assigned'
                courier.weight_of_food += order.weight

                db_sess.add(courier_order)
                db_sess.commit()
                ans.append({"id": order.order_id})
        db_sess.commit()

        print(ans)
        if len(ans) == 0:
            return jsonify([])

        if not courier.completed_flag:
            assign_time = str(time)
            courier.assign_time = assign_time
            db_sess.commit()
        else:
            assign_time = courier.assign_time

        data = {"order": ans,  'assign_time': assign_time}
        return make_response(jsonify(data), 200)


class OrderComplete(Resource):
    def post(self):
        db_sess = db_session.create_session()


        # try:
        args = complete_parser.parse_args()
        courier = db_sess.query(Courier).filter(Courier.courier_id == args['courier_id']).first()

        order = db_sess.query(Orders).filter(Orders.order_id == args['order_id']).first()
        complete_time = args["complete_time"]
        order.flag = 'completed'
        # db_sess.commit()

        if not courier or not order or not complete_time:
            abort(400, message='Bad Request')

        courier_to_order = db_sess.query(CourierToOrder).filter(CourierToOrder.courier_id == args['courier_id'],
                                                                CourierToOrder.order_id == args['order_id']).first()
        if not courier_to_order:
            abort(400, message='Bad Request')

        time = arrow.get(complete_time).datetime
        print(time)
        courier_to_order.completed_time = time
        db_sess.commit()
        #
        delta = courier_to_order.completed_time - courier_to_order.assigned_time
        print(delta.total_seconds())

        courier_to_region = db_sess.query(CourierToRegion).filter(CourierToRegion.courier_id == courier.courier_id,
                                                                  CourierToRegion.region_id == order.region).first()
        t = courier_to_region.time
        courier_to_region.time = t + delta.total_seconds()
        c = courier_to_region.count
        courier_to_region.count = c + 1
        db_sess.commit()

        lines = db_sess.query(CourierToRegion).filter(CourierToRegion.courier_id == courier.courier_id).all()
        times = map(lambda reg: reg.time, lines)
        t = min(times)
        rating = (60 * 60 - min(t, 60 * 60)) / (60 * 60) * 5

        courier.rating = rating
        db_sess.commit()

        if courier.courier_type == 'foot':
            C = 2
        elif courier.courier_type == 'bike':
            C = 5
        else:
            C = 9

        earnings = courier.earnings
        courier.earnings = earnings + 500 * C
        courier.completed_flag = True
        db_sess.commit()

        return make_response(jsonify({"order_id": order.order_id}), 200)

        # except Exception:
        #     abort(400, message='Bad Request')
