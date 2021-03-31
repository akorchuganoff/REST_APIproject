import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Courier(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Couriers'

    courier_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    courier_type = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    regions = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    working_hours = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    rating = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=None)
    earnings = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=False)

    def __repr__(self):
        return [{'Couriers_id': self.courier_id}, {'Courier_type': self.courier_type}, {'Regions': self.regions},
                {'Working hours': self.working_hours}, {'Rating': self.rating}, {'earnings': self.earnings}]
