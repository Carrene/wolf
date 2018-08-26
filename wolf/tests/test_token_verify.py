import unittest

from nanohttp import settings
from bddrest.authoring import when, response, status

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
        mockup_token1 = Token()
        mockup_token1.name = 'name1'
        mockup_token1.phone = 1
        mockup_token1.expire_date = '2059-12-07T18:14:39'
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

        mockup_token2 = Token()
        mockup_token2.name = 'name2'
        mockup_token2.phone = 2
        mockup_token2.expire_date = '2059-12-07T18:14:39'
        mockup_token2.seed = \
            b'u*1\'D\xb9\xbb\xa6Z.>\x88j\xbeZ\x9b3\xc6\xca\x84%\x87\n\x89' \
            b'\r\x8a\ri\x94(\xf2"H\xb0\xf7\x87\x9a\xa1I9\x01U\x81!\xd8\x9cg' \
            b'\xfc\xf7\xde\xe5\x13\xfb\xbaZ\xef\xa6dv\xa2\xc0Y\x00v'
        mockup_token2.is_active = True

        mockup_token3 = Token()
        mockup_token3.name = 'DeactivatedToken'
        mockup_token3.phone = 2
        mockup_token3.expire_date = '2059-12-07T18:14:39'
        mockup_token3.seed = \
            b'u*1\'D\xb9\xcb\xa6Z.>\x88j\xbeZ\x9b3\xc6\xca\x84%\x87\n\x89' \
            b'\r\x8a\ri\x94(\xf2"H\xb0\xf7\x87\x9a\xa1I9\x01U\x81!\xd8\x9cg' \
            b'\xfc\xf7\xde\xe5\x13\xfb\xbaZ\xef\xa6dv\xa2\xc0Y\x00v'
        mockup_token3.is_active = False

        # 752a312744b9bba65a2e3e886abe5a9b33c6ca8425870a890d8a0d699428f22248
        # b0f7879aa1493901558121d89c67fcf7dee513fbba5aefa66476a2c0590076

        mockup_cryptomodule_length_5 = Cryptomodule()
        mockup_cryptomodule_length_5.challenge_response_length = 5
        mockup_cryptomodule_length_5.one_time_password_length = 5
        mockup_token2.cryptomodule = mockup_cryptomodule_length_5
        mockup_token3.cryptomodule = mockup_cryptomodule_length_5

        session.add(mockup_token2)
        session.add(mockup_token3)
        session.add(mockup_cryptomodule_length_5)
        session.commit()

        cls.mockup_token1_id = mockup_token1.id
        cls.mockup_token2_id = mockup_token2.id
        cls.mockup_token3_id = mockup_token3.id
        cls.pinblock = EncryptedISOPinBlock(mockup_token1.id)
        cls.fake_time1 = 10001000
        cls.challenge1 = 'testchallenge-1'
        cls.valid_otp_token1_time1 = cls.pinblock.encode('7110').decode()
        cls.invalid_otp_token1_time1 = cls.pinblock.encode('123456').decode()

        cls.fake_time2 = 199919998
        cls.challenge2 = 'testchallenge-2'
        cls.valid_otp_token1_time2 = cls.pinblock.encode('1251').decode()
        cls.invalid_otp_token1_time2 = cls.pinblock.encode('123456').decode()

        cls.invalid_fake_time = 123456

        cls.fake_time3 = 1515515295
        cls.valid_otp_token2_time1 = cls.pinblock.encode('88533').decode()

    def test_verify_token_otp_time_length_5(self):
        mockup_token_id = self.mockup_token2_id

        with TimeMonkeyPatch(self.fake_time3), self.given(
            'Verifying time based OTP',
            \
                f'/apiv1/tokens/token_id: {mockup_token_id}/codes/code: '
                f'{self.valid_otp_token2_time1}',
            'VERIFY',
        ):
            assert status == 200

    def test_verify_token_otp_time(self):
        mockup_token_id = self.mockup_token1_id

        with TimeMonkeyPatch(self.fake_time1), self.given(
            'Verifying time based OTP',
            \
                f'/apiv1/tokens/token_id: {mockup_token_id}/codes/code: '
                f'{self.valid_otp_token1_time1}',
            'VERIFY',
        ):
            assert status == 200

            when(
                'Trying to verify an invalid code',
                url_parameters=dict(
                    code=self.invalid_otp_token1_time1,
                    token_id=mockup_token_id
                )
            )
            assert status == 400

        with TimeMonkeyPatch(self.fake_time2), self.given(
            'SKIP: Verifying time base OTP',
            \
                f'/apiv1/tokens/token_id: {mockup_token_id}/codes/code: '
                f'{self.valid_otp_token1_time2}',
            'VERIFY',
        ):
            assert status == 200

            when(
                'Trying to verify an invalid code',
                url_parameters=dict(
                    code=self.invalid_otp_token1_time2,
                    token_id=mockup_token_id
                )
            )
            assert status == 400

        call = dict(
        )

        with TimeMonkeyPatch(self.invalid_fake_time), self.given(
            'Verifying in invalid time',
            \
                f'/apiv1/tokens/token_id: {mockup_token_id}/codes/code: '
                f'{self.valid_otp_token1_time2}',
            'VERIFY',

        ):
            assert status == 400

    def test_verify_token_expiration(self):
        mockup_token_id = self.mockup_token1_id

        call = dict(
        )

        with TimeMonkeyPatch(self.fake_time1), self.given(
            'SKIP: ensure the code is valid',
            \
                f'/apiv1/tokens/token_id: {mockup_token_id}/codes/code: '
                f'{self.valid_otp_token1_time1}',
            'VERIFY',
        ):
            assert status == 200

        future_time = 99999999999
        with TimeMonkeyPatch(future_time), self.given(
            'when time expired',
            \
                f'/apiv1/tokens/token_id: {mockup_token_id}/codes/code: '
                f'{self.valid_otp_token1_time1}',
            'VERIFY',
        ):
            assert status == 461

    def test_verify_token_deactivated(self):
        mockup_token_id = self.mockup_token3_id
        with TimeMonkeyPatch(self.fake_time1), self.given(
            'when time expired',
            \
                f'/apiv1/tokens/token_id: {mockup_token_id}/codes/code: '
                f'{self.valid_otp_token1_time1}',
            'VERIFY',
        ):
            assert status == 463

    def test_verify_malformed_code(self):
        mockup_token_id = self.mockup_token1_id

        with TimeMonkeyPatch(self.fake_time1), self.given(
            'When code has odd length',
            f'/apiv1/tokens/token_id: {mockup_token_id}/codes/code: badcode',
            'VERIFY',
        ):
            assert status == 400

            when(
                'When code is malformed',
                url=\
                    f'/apiv1/tokens/token_id: {mockup_token_id}/codes/code: '
                    f'1234567'
            )
            assert status == 400

