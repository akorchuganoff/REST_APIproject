from flask import jsonify, make_response
from flask_restful import reqparse, abort, Resource
from . import db_session
from .orders import Orders
from .couriers import Courier
from .regions import CourierToRegion
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


def check_time(courier, order):
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
            if sa <= eb and ea >= sb:
                return True
    return False


class OrderListResource(Resource):
    # noinspection PyMethodMayBeStatic
    def post(self):
        args = parser.parse_args()
        valid = []
        invalid = []
        db_sess = db_session.create_session()
        ORDERS = []
        for elem in args['data']:
            # noinspection PyBroadException
            try:
                order = Orders()
                if elem['order_id'] in list(map(lambda order: order.order_id, db_sess.query(Orders).all())):
                    raise Exception
                order.order_id = elem['order_id']
                order.weight = elem['weight']
                if order.weight > 50:
                    raise Exception
                order.region = elem['region']
                order.delivery_hours = ' '.join(elem['delivery_hours'])
                ORDERS.append(order)

                valid.append({'id': order.order_id})
            except BaseException:
                invalid.append(elem['order_id'])

        if len(invalid) != 0:
            data = {'message': 'Bad request', "validation_error": {"orders": invalid}}
            return make_response(jsonify(data), 400)

        for elem in ORDERS:
            db_sess.add(elem)
        db_sess.commit()
        data = {'message': 'Created', "orders": valid}
        return make_response(jsonify(data), 201)


class OrderAssign(Resource):
    # noinspection PyMethodMayBeStatic
    def post(self):
        db_sess = db_session.create_session()
        args = assign_parser.parse_args()
        print(args['courier_id'])
        courier = db_sess.query(Courier).filter(Courier.courier_id == args['courier_id']).first()
        if not courier:
            abort(400, message='Bad Request')
        print(2)
        reg = list(map(lambda c_to_r: c_to_r.region_id, db_sess.query(CourierToRegion).filter(
            CourierToRegion.courier_id == courier.courier_id).all()))
        print(reg)
        ORDERS = []
        time = datetime.datetime.now(datetime.timezone.utc)
        for order in db_sess.query(Orders).all():
            if order.region in reg and order.weight < courier.max_weight - courier.weight_of_food and\
                    order.flag is None and check_time(courier, order):
                ORDERS.append(order)

                courier_order = CourierToOrder()
                courier_order.courier = courier
                courier_order.order = order
                if not courier.completed_flag:
                    courier_order.assigned_time = time
                else:
                    courier_order.assigned_time = courier.assign_time

                order.flag = 'assigned'
                courier.weight_of_food += order.weight

                db_sess.add(courier_order)
                # ans.append({"id": order.order_id})
        db_sess.commit()

        orders = db_sess.query(CourierToOrder).filter(CourierToOrder.courier_id == courier.courier_id).all()
        order_list = list(map(lambda c_to_o: c_to_o.order_id, orders))
        ans = list(map(lambda x: {"id": x}, order_list))
        print(ans)
        if len(ORDERS) == 0:
            return jsonify({'orders': ans})

        if not courier.completed_flag:
            assign_time = str(time)
            courier.assign_time = time
            db_sess.commit()
        else:
            assign_time = courier.assign_time

        data = {"order": ans,  'assign_time': assign_time}
        return make_response(jsonify(data), 200)


class OrderComplete(Resource):
    # noinspection PyMethodMayBeStatic
    def post(self):
        db_sess = db_session.create_session()

        try:
            args = complete_parser.parse_args()
            courier = db_sess.query(Courier).filter(Courier.courier_id == args['courier_id']).first()

            order = db_sess.query(Orders).filter(Orders.order_id == args['order_id']).first()
            complete_time = args["complete_time"]

            # db_sess.commit()

            if not courier or not order or not complete_time:
                abort(400, message='Bad Request')

            courier_to_order = db_sess.query(CourierToOrder).filter(CourierToOrder.courier_id == args['courier_id'],
                                                                    CourierToOrder.order_id == args['order_id']).first()
            if not courier_to_order:
                abort(400, message='Bad Request')

            if order.flag != 'completed':
                order.flag = 'completed'

                time = arrow.get(complete_time).datetime
                courier_to_order.completed_time = time
                db_sess.commit()
                print(courier_to_order.assigned_time)
                print(courier_to_order.completed_time)
                #
                delta = courier_to_order.completed_time - courier_to_order.assigned_time

                courier_to_region = db_sess.query(CourierToRegion).filter(CourierToRegion.courier_id == courier.courier_id,
                                                                          CourierToRegion.region_id == order.region).first()
                t = courier_to_region.time
                courier_to_region.time = t + delta.total_seconds()
                c = courier_to_region.count
                courier_to_region.count = c + 1
                db_sess.commit()

                lines = db_sess.query(CourierToRegion).filter(CourierToRegion.courier_id == courier.courier_id).all()
                # times = map(lambda reg: reg.time / reg.count, lines)
                times = []
                for i in range(len(lines)):
                    if lines[i].count == 0:
                        continue
                    times.append(lines[i].time / lines[i].count)
                t = min(times)
                print(t)
                rating = (60 * 60 - min(t, 60 * 60)) / (60 * 60) * 5
                print(rating)
                courier.rating = rating
                db_sess.commit()

                if courier.courier_type == 'foot':
                    k = 2
                elif courier.courier_type == 'bike':
                    k = 5
                else:
                    k = 9

                courier.weight_of_food -= order.weight
                earnings = courier.earnings
                courier.earnings = earnings + 500 * k
                courier.completed_flag = True
                db_sess.commit()

            return make_response(jsonify({"order_id": order.order_id}), 200)

        except Exception:
            abort(400, message='Bad Request')
