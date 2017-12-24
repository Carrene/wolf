import unittest

from nanohttp import settings
from restfulpy.orm import DBSession
from restfulpy.testing.documentation import FormParameter

from wolf.models import Token, OathCryptomodule
from wolf.tests.helpers import WebTestCase, As, TimeMonkeyPatch, TokenCounterMonkeyPatch


class VerifyTokenTestCase(WebTestCase):
    url = '/apiv1/tokens'

    window_size = 10

    @classmethod
    def configure_app(cls):
        super().configure_app()
        settings.merge(
            f"""
            oath:
              window: {cls.window_size}
            """
        )

    @classmethod
    def mockup(cls):
        mockup_token1 = Token()
        mockup_token1.name = 'name1'
        mockup_token1.provider_reference = 1
        mockup_token1.client_reference = 1
        mockup_token1.expire_date = '2059-12-07T18:14:39'
        mockup_token1.seed = \
            b'\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5' \
            b'\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xf5j\xaaz'
        mockup_token1.is_active = True

        mockup_cryptomodule1 = OathCryptomodule()
        mockup_cryptomodule1.provider_reference = 1
        mockup_cryptomodule1.hash_algorithm = 'SHA-1'
        mockup_cryptomodule1.counter_type = 'time'
        mockup_cryptomodule1.time_interval = 60
        mockup_cryptomodule1.one_time_password_length = 4
        mockup_cryptomodule1.challenge_response_length = 6
        mockup_cryptomodule1.is_active = True

        mockup_token1.cryptomodule = mockup_cryptomodule1

        mockup_token2 = Token()
        mockup_token2.name = 'name1'
        mockup_token2.provider_reference = 1
        mockup_token2.client_reference = 1
        mockup_token2.expire_date = '2059-12-07T18:14:39'
        mockup_token2.counter = 368
        mockup_token2.seed = \
            b'\xaa\xaa\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab' \
            b'\x0b5\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xf5j\xac\xcc'
        mockup_token2.is_active = True

        mockup_cryptomodule2 = OathCryptomodule()
        mockup_cryptomodule2.provider_reference = 1
        mockup_cryptomodule2.hash_algorithm = 'SHA-256'
        mockup_cryptomodule2.counter_type = 'counter'
        mockup_cryptomodule2.time_interval = 120
        mockup_cryptomodule2.one_time_password_length = 6
        mockup_cryptomodule2.challenge_response_length = 4
        mockup_cryptomodule2.is_active = True

        mockup_token2.cryptomodule = mockup_cryptomodule2

        DBSession.add(mockup_token1)
        DBSession.add(mockup_cryptomodule1)
        DBSession.add(mockup_token2)
        DBSession.add(mockup_cryptomodule2)
        DBSession.commit()

        cls.mockup_token1_id = mockup_token1.id
        cls.mockup_token2_id = mockup_token2.id

        # token1 -> timer
        # token2 -> count

        cls.fake_time1 = 10001000
        cls.fake_counter_1 = 368
        cls.challenge1 = 'testchallenge-1'
        cls.valid_otp_token1_time1 = '7110'
        cls.invalid_otp_token1_time1 = '123456'
        cls.valid_cr_token1_time1 = '730625'
        cls.invalid_cr_token1_time1 = '123456'
        cls.valid_otp_token2_counter1 = '300459'
        cls.invalid_otp_token2_counter1 = '123456'
        cls.valid_cr_token2_counter1 = '4628'
        cls.invalid_cr_token2_counter1 = '123456'

        cls.fake_time2 = 199919998
        cls.fake_counter_2 = 23
        cls.challenge2 = 'testchallenge-2'
        cls.valid_otp_token1_time2 = '1251'
        cls.invalid_otp_token1_time2 = '123456'
        cls.valid_cr_token1_time2 = '214777'
        cls.invalid_cr_token1_time2 = '123456'
        cls.valid_otp_token2_counter2 = '204879'
        cls.invalid_otp_token2_counter2 = '123456'
        cls.valid_cr_token2_counter2 = '2589'
        cls.invalid_cr_token2_counter2 = '123456'

        cls.invalid_fake_time = 123456
        cls.invalid_fake_counter = 123456

    def test_verify_token_otp_time(self):
        mockup_token_id = self.mockup_token1_id

        with TimeMonkeyPatch(self.fake_time1):

            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                params=[
                    FormParameter('code', self.valid_otp_token1_time1, type_=str)
                ]
            )

            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                params=[
                    FormParameter('code', self.invalid_otp_token1_time1, type_=str)
                ],
                expected_status=409
            )

        # Test on another time
        with TimeMonkeyPatch(self.fake_time2):

            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                params=[
                    FormParameter('code', self.valid_otp_token1_time2, type_=str)
                ]
            )

            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                params=[
                    FormParameter('code', self.invalid_otp_token1_time2, type_=str)
                ],
                expected_status=409
            )

        # Invalid time
        with TimeMonkeyPatch(self.invalid_fake_time):
            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                params=[
                    FormParameter('code', self.valid_otp_token1_time2, type_=str)
                ],
                expected_status=409
            )

    def test_verify_token_otp_counter(self):
        mockup_token_id = self.mockup_token2_id

        with TokenCounterMonkeyPatch(self.session, mockup_token_id, self.fake_counter_1):
            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                params=[
                    FormParameter('code', self.valid_otp_token2_counter1, type_=str)
                ]
            )

            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                params=[
                    FormParameter('code', self.invalid_otp_token2_counter1, type_=str)
                ],
                expected_status=409
            )

        # Test on another counter
        with TokenCounterMonkeyPatch(self.session, mockup_token_id, self.fake_counter_2):
            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                params=[
                    FormParameter('code', self.valid_otp_token2_counter2, type_=str)
                ]
            )

            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                params=[
                    FormParameter('code', self.invalid_otp_token2_counter2, type_=str)
                ],
                expected_status=409
            )

        # Invalid counter
        with TokenCounterMonkeyPatch(self.session, mockup_token_id, self.invalid_fake_counter):
            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                params=[
                    FormParameter('code', self.invalid_otp_token2_counter2, type_=str),
                ],
                expected_status=409
            )

    def test_verify_token_cr_time(self):
        mockup_token_id = self.mockup_token1_id

        with TimeMonkeyPatch(self.fake_time1):

            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                params=[
                    FormParameter('code', self.valid_cr_token1_time1, type_=str),
                    FormParameter('challenge', 'testchallenge', type_=str),
                ]
            )

            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                params=[
                    FormParameter('code', self.invalid_cr_token1_time1, type_=str),
                    FormParameter('challenge', 'testchallenge', type_=str),
                ],
                expected_status=409
            )

        # Test on another time
        with TimeMonkeyPatch(self.fake_time2):

            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                params=[
                    FormParameter('code', self.valid_cr_token1_time2, type_=str),
                    FormParameter('challenge', 'testchallenge', type_=str),
                ]
            )

            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                params=[
                    FormParameter('code', self.invalid_cr_token1_time2, type_=str),
                    FormParameter('challenge', 'testchallenge', type_=str),
                ],
                expected_status=409
            )

        # Invalid challenge
        with TimeMonkeyPatch(self.invalid_fake_time):

            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                params=[
                    FormParameter('code', self.valid_cr_token1_time2, type_=str),
                    FormParameter('challenge', 'badchallenge', type_=str),
                ],
                expected_status=409
            )

        # Invalid time
        with TimeMonkeyPatch(self.invalid_fake_time):

            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                params=[
                    FormParameter('code', self.valid_cr_token1_time2, type_=str),
                    FormParameter('challenge', 'testchallenge', type_=str),
                ],
                expected_status=409
            )

    def test_verify_token_cr_counter(self):
        mockup_token_id = self.mockup_token2_id

        with TokenCounterMonkeyPatch(self.session, mockup_token_id, self.fake_counter_1):
            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                params=[
                    FormParameter('code', self.valid_cr_token2_counter1, type_=str),
                    FormParameter('challenge', 'testchallenge', type_=str),
                ]
            )

            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                params=[
                    FormParameter('code', self.invalid_cr_token2_counter1, type_=str),
                    FormParameter('challenge', 'testchallenge', type_=str),
                ],
                expected_status=409
            )

        # Test on another counter
        with TokenCounterMonkeyPatch(self.session, mockup_token_id, self.fake_counter_2):
            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                params=[
                    FormParameter('code', self.valid_cr_token2_counter2, type_=str),
                    FormParameter('challenge', 'testchallenge', type_=str),
                ]
            )

            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                params=[
                    FormParameter('code', self.invalid_cr_token2_counter2, type_=str),
                    FormParameter('challenge', 'testchallenge', type_=str),
                ],
                expected_status=409
            )

        # Invalid challenge
        with TokenCounterMonkeyPatch(self.session, mockup_token_id, self.fake_counter_2):
            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                params=[
                    FormParameter('code', self.valid_cr_token1_time2, type_=str),
                    FormParameter('challenge', 'badchallenge', type_=str),
                ],
                expected_status=409
            )

        # Invalid counter
        with TokenCounterMonkeyPatch(self.session, mockup_token_id, self.invalid_fake_counter):
            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                params=[
                    FormParameter('code', self.valid_cr_token1_time2, type_=str),
                    FormParameter('challenge', 'testchallenge', type_=str),
                ],
                expected_status=409
            )

    def test_verify_token_expiration(self):
        mockup_token_id = self.mockup_token1_id

        with TimeMonkeyPatch(self.fake_time1):

            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                doc=False,
                params=[
                    FormParameter('code', self.valid_otp_token1_time1)
                ]
            )

        future_time = 9999999999999999
        with TimeMonkeyPatch(future_time):

            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                doc=False,
                params=[
                    FormParameter('code', self.valid_otp_token1_time1)
                ],
                expected_status=409,
                expected_headers={
                    'x-reason': 'token-expired'
                }
            )

    def test_verify_token_counter_incremental(self):
        mockup_token_id = self.mockup_token2_id

        settings.merge(
            '''
            oath:
              window: 0
            '''
        )

        # 1. otp
        with TokenCounterMonkeyPatch(self.session, mockup_token_id, self.fake_counter_1):
            # It should be correct
            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                doc=False,
                params=[
                    FormParameter('code', self.valid_otp_token2_counter1)
                ]
            )

            # But the counter has been incremented and it should be wrong
            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                doc=False,
                params=[
                    FormParameter('code', self.valid_otp_token2_counter1)
                ],
                expected_status=409,
                expected_headers={
                    'x-reason': 'not-verified'
                }
            )

        # 1. cr
        with TokenCounterMonkeyPatch(self.session, mockup_token_id, self.fake_counter_1):
            # It should be correct
            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                doc=False,
                params=[
                    FormParameter('code', self.valid_cr_token2_counter1),
                    FormParameter('challenge', 'testchallenge'),
                ]
            )

            # But the counter has been incremented and it should be wrong
            self.request(
                As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                doc=False,
                params=[
                    FormParameter('code', self.valid_cr_token2_counter1),
                    FormParameter('challenge', 'testchallenge'),
                ],
                expected_status=409,
                expected_headers={
                    'x-reason': 'not-verified'
                }
            )


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
