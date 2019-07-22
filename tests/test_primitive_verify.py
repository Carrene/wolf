from datetime import datetime, timedelta

import redis
from bddrest import when, status, given
from nanohttp import settings

from .helpers import TimeMonkeyPatch, LocalApplicationTestCase
from wolf.cryptoutil import EncryptedISOPinBlock
from wolf.models import Token, Cryptomodule


class TestVerifyPrimitive(LocalApplicationTestCase):
    _redis = None


    __configuration__ = '''
      oath:
        window: 10
      token:
        redis:
          enabled: true
    '''

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        cls.active_token1 = active_token1 = Token()
        active_token1.name = 'name1'
        active_token1.phone = 1
        active_token1.bank_id = 2
        active_token1.expire_date = datetime.now() + timedelta(minutes=1)
        active_token1.seed = \
            b'\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz'
        active_token1.is_active = True
        mockup_cryptomodule_length_4 = Cryptomodule()
        active_token1.cryptomodule = mockup_cryptomodule_length_4
        session.add(active_token1)

        session.commit()

        cls.pinblock1 = EncryptedISOPinBlock(
            active_token1.id.bytes,
            active_token1.bank_id
        )
        cls.valid_time = 10001000
        cls.valid_otp_token1_time = cls.pinblock1.encode('7110').decode()
        cls.invalid_otp_token1_time = cls.pinblock1.encode('123456').decode()

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

    def setup(self):
        self.redis().flushdb()

    def test_primitive_verify(self):
        self.login_as_switchcard()

        with TimeMonkeyPatch(self.valid_time), self.given(
                'Verifying time based OPT with primitive yes query', \
                    f'/apiv1/tokens/token_id: {self.active_token1.id}/codes'
                    f'/code: {self.valid_otp_token1_time}',
                'VERIFY',
                query=dict(primitive='yes')
        ):
            assert status == 200

            when('Trying to verify with yes primitive query again')
            assert status == 200

            when(
                'Trying to verify with Yes primitive query',
                query=given | dict(primitive='Yes')
            )
            assert status == 200

            when(
                'Trying to verify with no primitive query',
                query=given | dict(primitive='no')
            )
            assert status == '604 Invalid code'

            when(
                'Trying to verify without primitive query again',
                query=given - 'primitive'
            )
            assert status == '604 Invalid code'

            when('Trying to verify with yes primitive query again')
            assert status == '604 Invalid code'

    def test_verify_primitive_no(self):
        self.login_as_switchcard()

        with TimeMonkeyPatch(self.valid_time), self.given(
                'Verifying time based OPT with no primitive query',
                \
                    f'/apiv1/tokens/token_id: {self.active_token1.id}/codes'
                    f'/code: {self.valid_otp_token1_time}',
                'VERIFY',
                query=dict(primitive='no')
        ):
            assert status == 200

            when(
                'Trying to verify with yes primitive query again',
                query=given | dict(primitive='yes')
            )
            assert status == '604 Invalid code'

            when(
                'Trying to verify with no primitive query again',
                query=given | dict(primitive='no')
            )
            assert status == '604 Invalid code'

            when(
                'Trying to verify without primitive query',
                query=given - 'primitive'
            )
            assert status == '604 Invalid code'

