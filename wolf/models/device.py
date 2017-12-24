import base64

from sqlalchemy import Integer, Binary, BigInteger
from restfulpy.orm import DeclarativeBase, ModifiedMixin, Field


class Device(ModifiedMixin, DeclarativeBase):
    __tablename__ = 'device'

    id = Field(Integer, primary_key=True, protected=True)

    reference_id = Field(BigInteger, unique=True, index=True)
    secret = Field('secret', Binary(32))

    def prepare_for_export(self, column, value):
        if column is self.__class__.secret:
            return column.key, base64.encodebytes(value)

        return super().prepare_for_export(column, value)
