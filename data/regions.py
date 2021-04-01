import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Regions(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'regions'

    region_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, primary_key=True, autoincrement=True)
    region = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    time = sqlalchemy.Column(sqlalchemy.Float, nullable=False, default=0)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)

    courier_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("couriers.courier_id"))
    courier = orm.relation('Courier', back_populates="regions")


    # def __repr__(self):
    #     return [{'Order_id': self.order_id}, {'Weight': self.weight}, {'Region': self.region},
    #             {'Delivery_hours hours': self.delivery_hours}, {'Flag': self.flag}]
