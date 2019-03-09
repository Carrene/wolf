import time
import unittest
from datetime import datetime, timedelta

from nanohttp import settings
from bddrest import when, response, status, given

from wolf.models import Token, Cryptomodule
from wolf.cryptoutil import EncryptedISOPinBlock
from wolf.tests.helpers import TimeMonkeyPatch, LocalApplicationTestCase


class TestVerifyPrimitive(LocalApplicationTestCase):

    __configuration__ = '''
      oath:
        window: 10
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

        cls.active_token2 = active_token2 = Token()
        active_token2.name = 'name2'
        active_token2.phone = 2
        active_token2.bank_id = 2
        active_token2.expire_date = datetime.now() + timedelta(minutes=1)
        active_token2.seed = \
            b'\x15\xfc\x00\x8bH\xb6j\xf4\x14\x88\x1fR\xb8\xa5\xe1%~3\xf4\x81'
        active_token2.is_active = True
        active_token2.cryptomodule = mockup_cryptomodule_length_4
        session.add(active_token2)

        cls.deactivated_token = deactivated_token = Token()
        deactivated_token.name = 'DeactivatedToken'
        deactivated_token.phone = 3
        deactivated_token.bank_id = 2
        deactivated_token.expire_date = datetime.now() + timedelta(minutes=1)
        deactivated_token.seed = \
            b'u*1\'D\xb9\xcb\xa6Z.>\x88j\xbeZ\x9b3\xc6\xca\x84%\x87\n\x89'
        deactivated_token.is_active = False
        deactivated_token.cryptomodule = mockup_cryptomodule_length_4
        session.add(deactivated_token)

        session.commit()

        cls.pinblock1 = EncryptedISOPinBlock(active_token1.id)
        cls.pinblock2 = EncryptedISOPinBlock(active_token2.id)
        cls.valid_time = 10001000
        cls.invalid_time = 123456
        cls.valid_otp_token1_time = cls.pinblock1.encode('7110').decode()
        cls.valid_otp_token2_time = cls.pinblock2.encode('7110').decode()
        cls.invalid_otp_token1_time = cls.pinblock1.encode('123456').decode()
        cls.invalid_otp_token2_time = cls.pinblock2.encode('123456').decode()

    def test_primitive_verify(self):
        with TimeMonkeyPatch(self.valid_time), self.given(
                'Verifying time based OPT with primitive yes query', \
                    f'/apiv1/tokens/token_id: {self.active_token1.id}/codes'
                    f'/code: {self.valid_otp_token1_time}',
                'VERIFY',
                query=dict(primitive='yes')
        ):
            assert status == 200

            when(
                'Trying to verify an invalid code',
                url_parameters=given | dict(
                    code=self.invalid_otp_token1_time,
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
                .filter(Token.id == self.active_token1.id) \
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
        with TimeMonkeyPatch(self.valid_time), self.given(
                'Verifying time based OPT with no primitive query',
                \
                    f'/apiv1/tokens/token_id: {self.active_token2.id}/codes'
                    f'/code: {self.valid_otp_token2_time}',
                'VERIFY',
                query=dict(primitive='no')
        ):
            assert status == 200

            when(
                'Trying to verify an invalid code',
                url_parameters=given | dict(
                    code=self.invalid_otp_token2_time,
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
                .filter(Token.id == self.active_token2.id) \
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

