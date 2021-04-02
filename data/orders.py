import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


# association_table_courier_to_order = sqlalchemy.Table(
#     'courier_to_order',
#     SqlAlchemyBase.metadata,
#     sqlalchemy.Column('order_id', sqlalchemy.Integer,
#                       sqlalchemy.ForeignKey('Orders.order_id')),
#     sqlalchemy.Column('courier_id', sqlalchemy.Integer,
#                       sqlalchemy.ForeignKey('couriers.courier_id')),
#     sqlalchemy.Column('assigned_time', sqlalchemy.String, nullable=False, default=''),
#     sqlalchemy.Column('completed_time', sqlalchemy.Float, nullable=False, default=0)
# )

class CourierToOrder(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'courier_to_order'

    id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, primary_key=True, autoincrement=True)
    order_id = sqlalchemy.Column('order_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('Orders.order_id'))
    courier_id = sqlalchemy.Column('courier_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('couriers.courier_id'))
    assigned_time = sqlalchemy.Column(sqlalchemy.String, nullable=False, default='')
    completed_time = sqlalchemy.Column(sqlalchemy.String, nullable=False, default='')

    courier = orm.relation("Courier")
    order = orm.relation("Orders")


    def __repr__(self):
        return [{'Order_id': self.order_id}, {'Weight': self.weight}, {'Region': self.region},
                {'Delivery_hours hours': self.delivery_hours}, {'Flag': self.flag}]


class Orders(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Orders'

    order_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, nullable=False)
    weight = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    region = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    delivery_hours = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    flag = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=None)

    orders = orm.relation("CourierToOrder", back_populates='order')


    def __repr__(self):
        return [{'Order_id': self.order_id}, {'Weight': self.weight}, {'Region': self.region},
                {'Delivery_hours hours': self.delivery_hours}, {'Flag': self.flag}]
