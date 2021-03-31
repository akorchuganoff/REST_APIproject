from flask import Flask
from flask_restful import Api
from data import couriers_resources
from data import order_resources

from data import db_session
from data.couriers import Courier


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
api = Api(app)

api.add_resource(couriers_resources.CourierResource, '/couriers/<int:id>')
api.add_resource(couriers_resources.CouriersListResource, '/couriers')

# api.add_resource(order_resources.OrderResource, '')
api.add_resource(order_resources.OrderListResource, '/orders')
api.add_resource(order_resources.OrderAssign, '/orders/assign')
api.add_resource(order_resources.OrderComplete, '/orders/complete')


def main():
    db_session.global_init("db/database.db")

    db_sess = db_session.create_session()


    # Добавить что то в базу данных вот так
    # courier = Courier()
    # courier.courier_id = 1
    # courier.courier_type = 'car'
    # courier.regions = '134'
    # courier.working_hours = '09:00-18:00'
    # db_sess.add(courier)
    # db_sess.commit()

    # Вот так производится выборка всех
    # for user in db_sess.query(Courier).all():
    #     print(user)

    # Вот так производится выборка по определенному критерию (WHERE)
    # for user in db_sess.query(Courier).filter(Courier.courier_id > 1):
    #     print(user)

    # Вот так производится удаление
    # db_sess.query(Courier).filter(Courier.courier_id == 1).delete()
    # db_sess.commit()

    app.run(port=80, host='127.0.0.1', debug=True)


if __name__ == '__main__':
    main()