import time
import unittest
from datetime import datetime, timedelta

from nanohttp import settings
from bddrest import when, response, status, given

from wolf.models import Token, Cryptomodule
from wolf.cryptoutil import EncryptedISOPinBlock
from wolf.tests.helpers import TimeMonkeyPatch, LocalApplicationTestCase


class TestVerifyToken(LocalApplicationTestCase):

    __configuration__ = '''
      oath:
        window: 10
    '''

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        cls.mockup_token1 = mockup_token1 = Token()
        mockup_token1.name = 'name1'
        mockup_token1.phone = 1
        mockup_token1.expire_date = datetime.now() + timedelta(minutes=1)
        mockup_token1.seed = \
            b'\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz' \
            b'\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz' \
            b'\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz' \
            b'\xf5j\xaaz'
        mockup_token1.is_active = True

        mockup_cryptomodule_length_4 = Cryptomodule()
        mockup_token1.cryptomodule = mockup_cryptomodule_length_4

        session.add(mockup_token1)
        session.add(mockup_cryptomodule_length_4)

        session.commit()

        cls.pinblock = EncryptedISOPinBlock(mockup_token1.id)
        cls.valid_time = 10001000
        cls.invalid_time = 123456
        cls.valid_otp_token1_time1 = cls.pinblock.encode('7110').decode()
        cls.invalid_otp_token1_time1 = cls.pinblock.encode('123456').decode()

    def test_verify_token_otp_time(self):
        real_time = time.time
        with TimeMonkeyPatch(self.valid_time), self.given(
            'Verifying time based OTP',
            \
                f'/apiv1/tokens/token_id: {self.mockup_token1.id}/codes/code: '
                f'{self.valid_otp_token1_time1}',
            'VERIFY',
        ):
            assert status == 200

            when(
                'Trying to verify an invalid code',
                url_parameters=given | dict(
                    code=self.invalid_otp_token1_time1,
                )
            )
            assert status == '604 Invalid code'

            with TimeMonkeyPatch(self.invalid_time):
                when('Verifying a valid code within invalid time span')
                assert status == '604 Invalid code'

            with TimeMonkeyPatch(real_time() + 30):
                when('When token is expired')
                assert status == '602 Token is expired'
#
#    def test_verify_token_deactivated(self):
#        mockup_token_id = self.mockup_token3_id
#        with TimeMonkeyPatch(self.fake_time1), self.given(
#            'when time expired',
#            \
#                f'/apiv1/tokens/token_id: {mockup_token_id}/codes/code: '
#                f'{self.valid_otp_token1_time1}',
#            'VERIFY',
#        ):
#            assert status == 463
#
#    def test_verify_malformed_code(self):
#        mockup_token_id = self.mockup_token1_id
#
#        with TimeMonkeyPatch(self.fake_time1), self.given(
#            'When code has odd length',
#            f'/apiv1/tokens/token_id: {mockup_token_id}/codes/code: badcode',
#            'VERIFY',
#        ):
#            assert status == 400
#
#            when(
#                'When code is malformed',
#                url=\
#                    f'/apiv1/tokens/token_id: {mockup_token_id}/codes/code: '
#                    f'1234567'
#            )
#            assert status == 400
#
#    def test_nonempty_form(self):
#        mockup_token_id = self.mockup_token1_id
#
#        with TimeMonkeyPatch(self.fake_time1), self.given(
#            'When code has odd length',
#            f'/apiv1/tokens/token_id: {mockup_token_id}/codes/code: badcode',
#            'VERIFY',
#            form=dict(a='b')
#        ):
#            assert status == '700 Form Not Allowed'
#
#    def test_verify_token_otp_time_length_5(self):
#        mockup_token_id = self.mockup_token2_id
#
#        with TimeMonkeyPatch(1515515295), self.given(
#            'Verifying time based OTP',
#            \
#                f'/apiv1/tokens/token_id: {mockup_token_id}/codes/code: '
#                f'{self.valid_otp_token2_time1}',
#            'VERIFY',
#        ):
#            assert status == 200
#
#
