# Story: Return valid code for multiple requests with primitive equals to 'yes'

# As a client
# In order to verify OTP
# I want to get a valid code

# Scenario 1: Client get OK for multiple requests
# Given token_id and code
# And primitive equals to 'yes' in query string
# When client request for verify
# Then client get OK
# When client request again
# Then clinet get OK again
# when client remove or change primitive and request again
# Then client get OK for last time

# Scenario 2: Client get OK just one time
# Given primitive equals to 'no'
# When client request for verify
# Then client get OK

import unittest

import redis
from nanohttp import settings
from bddrest.authoring import when, then, response
from restfulpy.orm import DBSession

from wolf.models import Token, Cryptomodule
from wolf.cryptoutil import EncryptedISOPinBlock
from wolf.tests.helpers import TimeMonkeyPatch, BDDTestClass


class PrimitiveVerifyTestCase(BDDTestClass):
    _redis = None

    @classmethod
    def configure_app(cls):
        super().configure_app()
        settings.merge('''
            oath:
              window: 10
            token:
              redis:
                enabled: true
        ''')

    @classmethod
    def mockup(cls):
        mockup_token1 = Token()
        mockup_token1.name = 'name1'
        mockup_token1.phone = 1
        mockup_token1.expire_date = '2059-12-07T18:14:39'
        mockup_token1.seed = \
            b'\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5' \
            b'\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xf5j\xaaz'
        mockup_token1.is_active = True

        mockup_cryptomodule_length_4 = Cryptomodule()
        mockup_token1.cryptomodule = mockup_cryptomodule_length_4

        DBSession.add(mockup_token1)
        DBSession.add(mockup_cryptomodule_length_4)

        DBSession.commit()

        cls.mockup_token1_id = mockup_token1.id
        cls.pinblock = EncryptedISOPinBlock(mockup_token1.id)
        cls.fake_time1 = 10001000
        cls.valid_otp_token1_time1 = cls.pinblock.encode('7110').decode()
        cls.invalid_otp_token1_time1 = cls.pinblock.encode('123456').decode()

    @staticmethod
    def create_blocking_redis_client():
        return redis.StrictRedis(
            host=settings.token.redis.host,
            port=settings.token.redis.port,
            db=settings.token.redis.db,
            password=settings.token.redis.password,
            max_connections=settings.token.redis.max_connections,
            socket_timeout=settings.token.redis.socket_timeout
        )

    @classmethod
    def redis(cls):
        if cls._redis is None:
            cls._redis = cls.create_blocking_redis_client()
        return cls._redis

    def setUp(self):
        self.redis().flushdb()

    def test_primitive_verify(self):
        mockup_token_id = self.mockup_token1_id

        call = dict(
            title='Verifying time based OTP',
            description='Verifying time based OTP',
            url=f'/apiv1/tokens/token_id: {mockup_token_id}/codes'\
                f'/code: {self.valid_otp_token1_time1}',
            verb='VERIFY',
            query=dict(primitive='yes')
        )

        with TimeMonkeyPatch(self.fake_time1), self.given(**call):
            then(response.status_code == 200)

            when('Trying to verify with yes primitive query again')
            then(response.status_code == 200)

            when(
                'Trying to verify with Yes primitive query',
                query=dict(primitive='Yes')
            )
            then(response.status_code ==200)

            when(
                'Trying to verify with no primitive query',
                query=dict(primitive='no')
            )
            then(response.status_code ==400)

            when(
                'Trying to verify without primitive query again',
                query=None
            )
            then(response.status_code == 400)

            when('Trying to verify with yes primitive query again')
            then(response.status_code == 400)


    def test_primitive_verify_no(self):
        mockup_token_id = self.mockup_token1_id

        call = dict(
            title='Verifying time based OTP',
            description='Verifying time based OTP',
            url=f'/apiv1/tokens/token_id: {mockup_token_id}/codes' \
                f'/code: {self.valid_otp_token1_time1}',
            verb='VERIFY',
            query=dict(primitive='no')
        )

        with TimeMonkeyPatch(self.fake_time1), self.given(**call):
            then(response.status_code == 200)

            when(
                'Trying to verify with no primitive query again',
                query=dict(primitive='yes')
            )
            then(response.status_code == 400)

            when(
                'Trying to verify with no primitive query',
                query=dict(primitive='no')
            )
            then(response.status_code ==400)

            when(
                'Trying to verify with no primitive query',
                query=None
            )
            then(response.status_code ==400)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
