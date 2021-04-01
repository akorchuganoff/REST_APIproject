import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
from .regions import Regions


class Courier(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'couriers'

    courier_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    courier_type = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    working_hours = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    rating = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=None)
    earnings = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=False)
    weight_of_food = sqlalchemy.Column(sqlalchemy.Float, default=0, nullable=False)
    # orders_id = sqlalchemy.Column(sqlalchemy.String, default='', nullable=False)

    max_weight = sqlalchemy.Column(sqlalchemy.Float, default=0)
    completed_flag = sqlalchemy.Column(sqlalchemy.Boolean, default=False, nullable=False)
    assign_time = sqlalchemy.Column(sqlalchemy.String, default='', nullable=False)

    regions = orm.relation("Regions", secondary="association", backref="couriers")
    orders = orm.relation("Orders", secondary="courier_to_order", backref="couriers")

    def __repr__(self):
        return [{'Couriers_id': self.courier_id}, {'Courier_type': self.courier_type}, {'Regions': self.regions},
                {'Working hours': self.working_hours}, {'Rating': self.rating}, {'earnings': self.earnings}, {'max': self.max_weight}]
