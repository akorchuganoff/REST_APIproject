from flask import jsonify, request
from flask_restful import reqparse, abort, Resource
from . import db_session
from .orders import Orders

parser = reqparse.RequestParser()
parser.add_argument('data', required=False, type=dict, action='append')


class OrderListResource(Resource):
    def post(self):
        db_sess = db_session.create_session()
        args = parser.parse_args()
        L = []
        for elem in args['data']:
            order = Orders()
            order.order_id = elem['order_id']
            order.weight = elem['weight']
            order.region = elem['region']
            order.delivery_hours = elem['delivery_hours']

            db_sess.add(order)
            db_sess.commit()

            order_get = db_sess.query(Orders).filter(Orders.order_id == elem['order_id']).first()
            L.append(order_get.to_dict())
        return jsonify(L)
