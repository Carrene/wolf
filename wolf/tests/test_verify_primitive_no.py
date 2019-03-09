import time
import unittest
from datetime import datetime, timedelta

from nanohttp import settings
from bddrest import when, response, status, given

from wolf.models import Token, Cryptomodule
from wolf.cryptoutil import EncryptedISOPinBlock
from wolf.tests.helpers import TimeMonkeyPatch, LocalApplicationTestCase


class TestVerifyNoPrimitive(LocalApplicationTestCase):

    __configuration__ = '''
      oath:
        window: 10
    '''

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        cls.active_token = active_token = Token()
        active_token.name = 'name1'
        active_token.phone = 1
        active_token.bank_id = 2
        active_token.expire_date = datetime.now() + timedelta(minutes=1)
        active_token.seed = \
            b'\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz'
        active_token.is_active = True

        mockup_cryptomodule_length_4 = Cryptomodule()
        active_token.cryptomodule = mockup_cryptomodule_length_4
        session.add(active_token)

        cls.deactivated_token = deactivated_token = Token()
        deactivated_token.name = 'DeactivatedToken'
        deactivated_token.phone = 2
        deactivated_token.bank_id = 2
        deactivated_token.expire_date = datetime.now() + timedelta(minutes=1)
        deactivated_token.seed = \
            b'u*1\'D\xb9\xcb\xa6Z.>\x88j\xbeZ\x9b3\xc6\xca\x84%\x87\n\x89'
        deactivated_token.is_active = False
        deactivated_token.cryptomodule = mockup_cryptomodule_length_4
        session.add(deactivated_token)

        session.commit()

        cls.pinblock = EncryptedISOPinBlock(active_token.id)
        cls.valid_time = 10001000
        cls.invalid_time = 123456
        cls.valid_otp_token_time = cls.pinblock.encode('7110').decode()
        cls.invalid_otp_token_time = cls.pinblock.encode('123456').decode()

    def test_verify_primitive_no(self):
        real_time = time.time
        with TimeMonkeyPatch(self.valid_time), self.given(
                'Verifying time based OPT with primitive yes query',
                \
                    f'/apiv1/tokens/token_id: {self.active_token.id}/codes'
                    f'/code: {self.valid_otp_token_time}',
                'VERIFY',
                query=dict(primitive='no')
        ):
            assert status == 200

            when(
                'Trying to verify an invalid code',
                url_parameters=given | dict(
                    code=self.invalid_otp_token_time,
                )
            )
            assert status == '604 Invalid code'

            when(
                'When code has odd length',
                url_parameters=given | dict(code='12345')
            )
            assert status == '604 Invalid code'

            when(
                'When code is malformed',
                url_parameters=given | dict(code='Ma!f0rM3&')
            )
            assert status == '604 Invalid code'

            when(
                'Token not exists',
                url_parameters=given | dict(
                    token_id=0,
                )
            )
            assert status == '404 Not Found'

            with TimeMonkeyPatch(self.invalid_time):
                when('Verifying a valid code within invalid time span')
                assert status == '604 Invalid code'

            session = self.create_session()
            token = session.query(Token) \
                .filter(Token.id == self.active_token.id) \
                .one()
            token.expire_date = datetime(1970, 3, 1)
            session.commit()
            when('When token is expired')
            assert status == '602 Token is expired'
            token.expire_date = datetime.now() + timedelta(days=1)
            session.commit()

            when(
                'Token is deactivated',
                url_parameters=given | dict(
                    token_id=self.deactivated_token.id
                ),
            )
            assert status == '603 Token is deactivated'

            when('Form is not empty', form=dict(a='b'))
            assert status == '400 Form Not Allowed'

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

