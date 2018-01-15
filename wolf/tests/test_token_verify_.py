import unittest

from nanohttp import settings
from restfulpy.orm import DBSession

from wolf.models import Token, Cryptomodule
from wolf.cryptoutil import EncryptedISOPinBlock
from wolf.tests.helpers import TimeMonkeyPatch, DocumentaryTestCase


class VerifyTokenTestCase(DocumentaryTestCase):

    @classmethod
    def application_factory(cls):
        app = super().application_factory()
        settings.merge('''
            oath:
              window: 10
        ''')
        return app

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

        mockup_token2 = Token()
        mockup_token2.name = 'name2'
        mockup_token2.phone = 2
        mockup_token2.expire_date = '2059-12-07T18:14:39'
        mockup_token2.seed = \
            b'u*1\'D\xb9\xbb\xa6Z.>\x88j\xbeZ\x9b3\xc6\xca\x84%\x87\n\x89\r\x8a\ri\x94(\xf2"H\xb0\xf7\x87\x9a\xa1I9' \
            b'\x01U\x81!\xd8\x9cg\xfc\xf7\xde\xe5\x13\xfb\xbaZ\xef\xa6dv\xa2\xc0Y\x00v'
        mockup_token2.is_active = True

        # 752a312744b9bba65a2e3e886abe5a9b33c6ca8425870a890d8a0d699428f22248b0f7879aa1493901558121d89c67fcf7dee513fbba5aefa66476a2c0590076

        mockup_cryptomodule_length_5 = Cryptomodule()
        mockup_cryptomodule_length_5.challenge_response_length = 5
        mockup_cryptomodule_length_5.one_time_password_length = 5
        mockup_token2.cryptomodule = mockup_cryptomodule_length_5

        DBSession.add(mockup_token2)
        DBSession.add(mockup_cryptomodule_length_5)
        DBSession.commit()

        cls.mockup_token1_id = mockup_token1.id
        cls.mockup_token2_id = mockup_token2.id
        cls.pinblock = EncryptedISOPinBlock(mockup_token1.id)
        cls.fake_time1 = 10001000
        cls.challenge1 = 'testchallenge-1'
        cls.valid_otp_token1_time1 = cls.pinblock.encode('7110')
        cls.invalid_otp_token1_time1 = cls.pinblock.encode('123456')

        cls.fake_time2 = 199919998
        cls.challenge2 = 'testchallenge-2'
        cls.valid_otp_token1_time2 = cls.pinblock.encode('1251')
        cls.invalid_otp_token1_time2 = cls.pinblock.encode('123456')

        cls.invalid_fake_time = 123456

        cls.fake_time3 = 1515515295
        cls.valid_otp_token2_time1 = cls.pinblock.encode('88533')

    def test_verify_token_otp_time_length_5(self):
        mockup_token_id = self.mockup_token2_id

        with TimeMonkeyPatch(self.fake_time3):

            self.call_as_bank(
                'Verifying time based OTP',
                'VERIFY',
                f'/apiv1/tokens/token_id: {mockup_token_id}/codes/code: {self.valid_otp_token2_time1}',
            )

    def test_verify_token_otp_time(self):
        mockup_token_id = self.mockup_token1_id

        with TimeMonkeyPatch(self.fake_time1):

            self.call_as_bank(
                'Verifying time based OTP',
                'VERIFY',
                f'/apiv1/tokens/token_id: {mockup_token_id}/codes/code: {self.valid_otp_token1_time1}',
            )

            self.call_as_bank(
                'Trying to verify an invalid code',
                'VERIFY',
                f'/apiv1/tokens/token_id: {mockup_token_id}/codes/code: {self.invalid_otp_token1_time1}',
                status=400,
            )

        # Test on another time
        with TimeMonkeyPatch(self.fake_time2):
            self.call_as_bank(
                'SKIP: Verifying time base OTP',
                'VERIFY',
                f'/apiv1/tokens/token_id: {mockup_token_id}/codes/code: {self.valid_otp_token1_time2}',
            )

            self.call(
                'SKIP: Trying to verify an invalid code',
                'VERIFY',
                f'/apiv1/tokens/token_id: {mockup_token_id}/codes/code: {self.invalid_otp_token1_time2}',
                status=400,
            )

        # Invalid time
        with TimeMonkeyPatch(self.invalid_fake_time):
            self.call(
                'Verifying in invalid time',
                'VERIFY',
                f'/apiv1/tokens/token_id: {mockup_token_id}/codes/code: {self.valid_otp_token1_time2}',
                status=400,
            )

    def test_verify_token_expiration(self):
        mockup_token_id = self.mockup_token1_id

        with TimeMonkeyPatch(self.fake_time1):
            self.call(
                'SKIP: ensure the code is valid',
                'VERIFY',
                f'/apiv1/tokens/token_id: {mockup_token_id}/codes/code: {self.valid_otp_token1_time1}',
            )

        future_time = 99999999999
        with TimeMonkeyPatch(future_time):
            self.call(
                'When time expired',
                'VERIFY',
                f'/apiv1/tokens/token_id: {mockup_token_id}/codes/code: {self.valid_otp_token1_time1}',
                status=461
            )


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
