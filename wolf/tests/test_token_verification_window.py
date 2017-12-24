import unittest

from nanohttp import settings
from restfulpy.orm import DBSession
from restfulpy.testing.documentation import FormParameter

from wolf.models import Token, OathCryptomodule
from wolf.tests.helpers import WebTestCase, As, TimeMonkeyPatch, TokenCounterMonkeyPatch


class TokenWindowVerificationTestCase(WebTestCase):
    url = '/apiv1/tokens'

    time_interval = 60
    window_size = 5

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
        mockup_time_token = Token()
        mockup_time_token.name = 'name1'
        mockup_time_token.provider_reference = 1
        mockup_time_token.client_reference = 1
        mockup_time_token.expire_date = '2059-12-07T18:14:39'
        mockup_time_token.seed = \
            b'\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5' \
            b'\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xf5j\xaaz'
        mockup_time_token.is_active = True

        mockup_time_cryptomodule = OathCryptomodule()
        mockup_time_cryptomodule.provider_reference = 1
        mockup_time_cryptomodule.hash_algorithm = 'SHA-1'
        mockup_time_cryptomodule.counter_type = 'time'
        mockup_time_cryptomodule.time_interval = cls.time_interval
        mockup_time_cryptomodule.one_time_password_length = 4
        mockup_time_cryptomodule.challenge_response_length = 6
        mockup_time_cryptomodule.is_active = True

        mockup_time_token.cryptomodule = mockup_time_cryptomodule

        mockup_counter_token = Token()
        mockup_counter_token.name = 'name1'
        mockup_counter_token.provider_reference = 1
        mockup_counter_token.client_reference = 1
        mockup_counter_token.expire_date = '2059-12-07T18:14:39'
        mockup_counter_token.counter = 368
        mockup_counter_token.seed = \
            b'\xaa\xaa\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab' \
            b'\x0b5\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xf5j\xac\xcc'
        mockup_counter_token.is_active = True

        mockup_counter_cryptomodule = OathCryptomodule()
        mockup_counter_cryptomodule.provider_reference = 1
        mockup_counter_cryptomodule.hash_algorithm = 'SHA-256'
        mockup_counter_cryptomodule.counter_type = 'counter'
        mockup_counter_cryptomodule.time_interval = cls.time_interval
        mockup_counter_cryptomodule.one_time_password_length = 6
        mockup_counter_cryptomodule.challenge_response_length = 4
        mockup_counter_cryptomodule.is_active = True

        mockup_counter_token.cryptomodule = mockup_counter_cryptomodule

        DBSession.add(mockup_time_token)
        DBSession.add(mockup_time_cryptomodule)
        DBSession.add(mockup_counter_token)
        DBSession.add(mockup_counter_cryptomodule)
        DBSession.commit()

        cls.valid_time_otp = '7110'
        cls.valid_time_cr = '372767'
        cls.valid_counter_otp = '300459'
        cls.valid_counter_cr = '3827'

        cls.mockup_time_token_id = mockup_time_token.id
        cls.mockup_counter_token_id = mockup_counter_token.id

        cls.fake_time = 10001000
        cls.fake_counter = 368
        cls.mockup_challenge = 'goodchallenge'

    def test_verify_window_time_token(self):
        mockup_token_id = self.mockup_time_token_id

        # 1. otp mode
        with TimeMonkeyPatch(self.fake_time) as time_monkey_patch:

            for i in range(self.window_size * 2 + 3):
                arranged_i = (-self.window_size + i - 1)
                time_monkey_patch.fake_time = self.time_interval * arranged_i + self.fake_time
                self.request(
                    As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                    doc=False,
                    params=[
                        FormParameter('code', self.valid_time_otp, type_=str)
                    ], expected_status=200 if -self.window_size <= arranged_i <= self.window_size else 409
                )

        # 2. cr mode
        with TimeMonkeyPatch(self.fake_time) as time_monkey_patch:

            for i in range(self.window_size * 2 + 3):
                arranged_i = (-self.window_size + i - 1)
                time_monkey_patch.fake_time = self.time_interval * arranged_i + self.fake_time
                self.request(
                    As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                    doc=False,
                    params=[
                        FormParameter('code', self.valid_time_cr, type_=str),
                        FormParameter('challenge', self.mockup_challenge, type_=str)
                    ], expected_status=200 if -self.window_size <= arranged_i <= self.window_size else 409
                )

    def test_verify_window_counter_token(self):
        mockup_token_id = self.mockup_counter_token_id

        # 1. otp mode
        with TokenCounterMonkeyPatch(self.session, mockup_token_id, self.fake_counter) as counter_monkey_patch:
            for i in range(self.window_size * 2 + 3):
                arranged_i = (-self.window_size + i - 1)
                counter_monkey_patch.set_fake_counter(arranged_i + self.fake_counter)
                self.request(
                    As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                    doc=False,
                    params=[
                        FormParameter('code', self.valid_counter_otp, type_=str)
                    ], expected_status=200 if -self.window_size <= arranged_i <= self.window_size else 409
                )

        # 2. cr mode
        with TokenCounterMonkeyPatch(self.session, mockup_token_id, self.fake_counter) as counter_monkey_patch:
            for i in range(self.window_size * 2 + 3):
                arranged_i = (-self.window_size + i - 1)
                counter_monkey_patch.set_fake_counter(arranged_i + self.fake_counter)
                self.request(
                    As.provider, 'VERIFY', f'{self.url}/{mockup_token_id}/codes',
                    doc=False,
                    params=[
                        FormParameter('code', self.valid_counter_cr, type_=str),
                        FormParameter('challenge', self.mockup_challenge, type_=str)
                    ], expected_status=200 if -self.window_size <= arranged_i <= self.window_size else 409
                )


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
