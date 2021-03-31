import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Courier(SqlAlchemyBase):
    __tablename__ = 'Couriers'

    courier_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    courier_type = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    regions = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    working_hours = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    rating = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=None)
    earnings = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=False)

    def __repr__(self):
        return f'\nNEW COURIER\nCouriers_id: {self.courier_id}\nCourier_type: {self.courier_type}\nRegions: {self.regions}\nWor' \
               f'king hours: {self.working_hours}\nRating: {self.rating}\nearnings: {self.earnings}'
