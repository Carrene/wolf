from restfulpy.orm import Field, ModifiedMixin, PaginationMixin, DeclarativeBase, AutoActivationMixin, FilteringMixin, \
    OrderingMixin
from sqlalchemy import Integer, Enum, Unicode
from sqlalchemy.orm import validates

from oathpy import OCRASuite


class Cryptomodule(AutoActivationMixin, ModifiedMixin, PaginationMixin, FilteringMixin, OrderingMixin, DeclarativeBase):
    __tablename__ = 'cryptomodule'

    id = Field(Integer, primary_key=True)
    provider_reference = Field(Integer, index=True, default=0)

    type = Field(Unicode(50))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': __tablename__
    }


class OathCryptomodule(Cryptomodule):
    __mapper_args__ = {
        'polymorphic_identity': 'oath',
    }

    hash_algorithm = Field(
        Enum('SHA-1', 'SHA-256', 'SHA-384', 'SHA-512', name='cryptomodule_hash_algorithm'), default='SHA-1'
    )
    counter_type = Field(Enum('time', 'counter', name='cryptomodule_counter_type'), default='time')
    time_interval = Field(Integer, default=60)
    one_time_password_length = Field(Integer, default=4)
    challenge_response_length = Field(Integer, default=6)

    @validates('time_interval')
    def validate_time_interval(self, key, new_value):
        if new_value == 0:
            raise ValueError('Time interval should not be zero')
        elif 60 <= new_value <= 59 * 60 and new_value % 60 != 0:
            raise ValueError('60 <= time_interval <= 59 * 60 and time_interval % 60 != 0')
        elif 60 * 60 <= new_value <= (48 * 60 * 60) and new_value % (60 * 60) != 0:
            raise ValueError('60 <= time_interval <= 59 * 60 and time_interval % 60 != 0')
        return new_value

    @validates('challenge_limit')
    def validate_challenge_limit(self, key, new_value):
        if not 4 <= new_value <= 64:
            raise ValueError('Challenge limit value must be between 4-64')
        return new_value

    @validates('one_time_password_length')
    def validate_one_time_password(self, key, new_value):
        new_value = int(new_value)
        if not 4 <= new_value <= 10:
            raise ValueError('Length should be between 4 and 10')
        return new_value

    @validates('challenge_response_length')
    def validate_challenge_response_length(self, key, new_value):
        new_value = int(new_value)
        if not 4 <= new_value <= 10:
            raise ValueError('Length should be between 4 and 10')
        return new_value

    @validates('hash_algorithm')
    def validate_hash_algorithm(self, key, new_value):
        if new_value not in ['SHA-1', 'SHA-256', 'SHA-384', 'SHA-512']:
            raise ValueError('This hash type does not supported')
        return new_value

    @property
    def ocra_suite(self):
        return (OCRASuite(
            counter_type=self.counter_type,
            length=self.challenge_response_length,
            hash_algorithm=self.hash_algorithm,
            time_interval=self.time_interval if self.counter_type == 'time' else None,
        ))

    def to_dict(self):
        result = super().to_dict()
        result['ocraSuite'] = self.ocra_suite
        return result
