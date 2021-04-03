from flask import Flask
from flask_restful import Api
from data import couriers_resources
from data import order_resources
from data import db_session
from waitress import serve


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
api = Api(app)

api.add_resource(couriers_resources.CourierResource, '/couriers/<int:id>')
api.add_resource(couriers_resources.CouriersListResource, '/couriers')

api.add_resource(order_resources.OrderListResource, '/orders')
api.add_resource(order_resources.OrderAssign, '/orders/assign')
api.add_resource(order_resources.OrderComplete, '/orders/complete')


def main():
    db_session.global_init("db/database.db")
    serve(app, port=80, host='127.0.0.1')


if __name__ == '__main__':
    main()
