import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


# association_table = sqlalchemy.Table(
#     'association',
#     SqlAlchemyBase.metadata,
#     sqlalchemy.Column('region', sqlalchemy.Integer,
#                       sqlalchemy.ForeignKey('regions.region')),
#     sqlalchemy.Column('courier_id', sqlalchemy.Integer,
#                       sqlalchemy.ForeignKey('couriers.courier_id')),
#     sqlalchemy.Column('time', sqlalchemy.Integer, default=0, nullable=False),
#     sqlalchemy.Column('count', sqlalchemy.Integer, default=0, nullable=False)
# )


class CourierToRegion(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'courier_to_region'

    id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, primary_key=True, autoincrement=True)

    region_id = sqlalchemy.Column('region', sqlalchemy.Integer, sqlalchemy.ForeignKey('regions.region'))
    courier_id = sqlalchemy.Column('courier_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('couriers.courier_id'))

    time = sqlalchemy.Column('time', sqlalchemy.Integer, default=0, nullable=False)
    count = sqlalchemy.Column('count', sqlalchemy.Integer, default=0, nullable=False)

    courier = orm.relation("Courier")
    region = orm.relation("Regions")


class Regions(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'regions'

    region = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, primary_key=True, autoincrement=True)
    orders = orm.relation("CourierToRegion", back_populates='region')

    def __repr__(self):
        return f'region : {self.region}'

    def __str__(self):
        return f'region : {self.region}'