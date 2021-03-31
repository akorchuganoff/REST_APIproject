import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Courier(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Orders'

    order_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    weight = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    region = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    delivery_hours = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    flag = sqlalchemy.Column(sqlalchemy.String, nullable=False)


    def __repr__(self):
        return [{'Order_id': self.order_id}, {'Weight': self.weight}, {'Region': self.region},
                {'Delivery_hours hours': self.delivery_hours}, {'Flag': self.flag}]
