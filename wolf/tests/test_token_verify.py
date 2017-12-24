import unittest

from nanohttp import settings
from restfulpy.orm import DBSession

from wolf.models import Token, Cryptomodule
from wolf.tests.helpers import WebTestCase, As, TimeMonkeyPatch


class VerifyTokenTestCase(WebTestCase):
    url = '/apiv1/tokens'

    @classmethod
    def configure_app(cls):
        super().configure_app()
        settings.merge('''
            oath:
              window: 10
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

        mockup_cryptomodule1 = Cryptomodule()
        mockup_token1.cryptomodule = mockup_cryptomodule1

        DBSession.add(mockup_token1)
        DBSession.add(mockup_cryptomodule1)
        DBSession.commit()

        cls.mockup_token1_id = mockup_token1.id

        cls.fake_time1 = 10001000
        cls.challenge1 = 'testchallenge-1'
        cls.valid_otp_token1_time1 = '7110'
        cls.invalid_otp_token1_time1 = '123456'

        cls.fake_time2 = 199919998
        cls.challenge2 = 'testchallenge-2'
        cls.valid_otp_token1_time2 = '1251'
        cls.invalid_otp_token1_time2 = '123456'

        cls.invalid_fake_time = 123456

    def test_verify_token_otp_time(self):
        mockup_token_id = self.mockup_token1_id

        with TimeMonkeyPatch(self.fake_time1):

            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes/{self.valid_otp_token1_time1}',
            )

            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes/{self.invalid_otp_token1_time1}',
                expected_status=400
            )

        # Test on another time
        with TimeMonkeyPatch(self.fake_time2):

            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes/{self.valid_otp_token1_time2}',
            )

            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes/{self.invalid_otp_token1_time2}',
                expected_status=400
            )

        # Invalid time
        with TimeMonkeyPatch(self.invalid_fake_time):
            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes/{self.valid_otp_token1_time2}',
                expected_status=400
            )

    def test_verify_token_expiration(self):
        mockup_token_id = self.mockup_token1_id

        with TimeMonkeyPatch(self.fake_time1):

            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes/{self.valid_otp_token1_time1}',
            )

        future_time = 9999999999999999
        with TimeMonkeyPatch(future_time):

            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes/{self.valid_otp_token1_time1}',
                expected_status=409,
                expected_headers={
                    'x-reason': 'token-expired'
                }
            )


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
