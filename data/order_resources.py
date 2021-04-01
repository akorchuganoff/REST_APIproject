from flask import jsonify, request, make_response
from flask_restful import reqparse, abort, Resource
from . import db_session
from .orders import Orders
from .couriers import Courier
from .regions import Regions
from .orders import association_table_courier_to_order
import datetime

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
        reg = list(map(lambda region: region.region, courier.regions))
        # regions = list(map(int, courier.regions.split(' ')))
        print(reg)
        ans = []
        for order in db_sess.query(Orders).all():
            # L.append(order.flag)
            if order.region in reg and order.weight < courier.max_weight - courier.weight_of_food and order.flag == None and checkTime(courier, order):
                # return jsonify(order.region)
                # L.append(str(order.order_id))
                courier.orders.append(order)
                order.flag = 'assigned'
                courier.weight_of_food += order.weight
                db_sess.commit()
                ans.append({"id": order.order_id})
        # courier.orders_id += ' '.join(L)
        db_sess.commit()

        print(ans)
        if len(ans) == 0:
            return jsonify([])

        if not courier.completed_flag:
            assign_time = str(datetime.datetime.now())
            courier.assign_time = assign_time
            courier.completed_flag = True
            db_sess.commit()
        else:
            assign_time = courier.assign_time

        db_sess = db_session.create_session()
        assotiates = db_sess.query(association_table_courier_to_order).filter(association_table_courier_to_order.c.courier_id == courier.courier_id).all()
        # assotiates.assigned_time
        for elem in assotiates:
            elem.assigned_time = assign_time
            db_sess.commit()
        data = {"order": ans,  'assign_time': assign_time}
        return make_response(jsonify(data), 200)


class OrderComplete(Resource):
    def post(self):
        db_sess = db_session.create_session()

        # try:
        args = complete_parser.parse_args()
        ident = args['courier_id']
        courier = db_sess.query(Courier).filter(Courier.courier_id == ident).first()
        # courier = db_sess.query(Courier).filter(Courier.courier_id == args['courier_id']).first()
        return jsonify(courier.to_dict())
        # order = db_sess.query(Orders).filter(Orders.order_id == args['order_id']).first()
        # complete_time = args["complete_time"]
        #
        #
        # if not courier or not order or not complete_time:
        #     abort(400, message='Bad Request')
        #
        # reg = db_sess.query(Regions).filter(Regions.region == order.region, Regions.courier_id == courier.courier_id).first()
        # time = courier.assign_time
        #
        # return jsonify({'time': time})

        # except Exception:
        #     abort(400, message='Bad Request')
