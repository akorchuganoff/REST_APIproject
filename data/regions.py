import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


association_table = sqlalchemy.Table(
    'association',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('region', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('regions.region')),
    sqlalchemy.Column('courier_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('couriers.courier_id')),
    sqlalchemy.Column('time', sqlalchemy.Integer, default=0, nullable=False),
    sqlalchemy.Column('count', sqlalchemy.Integer, default=0, nullable=False)
)


class Regions(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'regions'

    region = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, primary_key=True, autoincrement=True)

    def __repr__(self):
        return [{'region': self.region}]
