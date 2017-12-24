import unittest

from restfulpy.orm import DBSession
from restfulpy.testing.documentation import FormParameter

from wolf.models import Token, OathCryptomodule
from wolf.tests.helpers import WebTestCase, As, RandomMonkeyPatch

mockup_seed = \
    b'\xdaa\xff\x8a6a\xff\x86\x8fV\xaa\xa7\x86\x8fV\xaa\xa7\xa4V\x8a6\x1f\xf8\xa6\x1f\xf8\xa3\xff\x8a;\x06\xab\x0b5' \
    b'\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8fV\xaa\xa7\xad\xa4X\xf5j\xaaz\xf5j\xaaz'


# https://github.com/Carrene/wolf/wiki/User-Stories#reseed-token
class TokenSeedTestCase(WebTestCase):
    url = '/apiv1/tokens'

    @classmethod
    def mockup(cls):
        mockup_cryptomodule = OathCryptomodule()

        cls.mockup_token1_initial_seed = \
            b'\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5' \
            b'\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xf5j\xaaz'

        cls.mockup_token2_initial_seed = \
            b'\xda!\x9e\xb6a\xffffffffffffffffffffffffffff\x0b5\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab' \
            b'\x0b5\xf8h\x88\x88\x88\x8a\xf5j\xaaz'

        mockup_token1 = Token()
        mockup_token1.name = 'name1'
        mockup_token1.provider_reference = 1
        mockup_token1.client_reference = 1
        mockup_token1.expire_date = '2099-12-07T18:14:39'
        mockup_token1.seed = cls.mockup_token1_initial_seed
        mockup_token1.is_active = True
        mockup_token1.cryptomodule = mockup_cryptomodule

        mockup_token2 = Token()
        mockup_token2.name = 'name2'
        mockup_token2.provider_reference = 1
        mockup_token2.client_reference = 1
        mockup_token2.expire_date = '2089-12-07T18:14:39'
        mockup_token2.seed = cls.mockup_token2_initial_seed
        mockup_token2.is_active = True
        mockup_token2.cryptomodule = mockup_cryptomodule

        DBSession.add(mockup_token1)
        DBSession.add(mockup_token2)
        DBSession.commit()

        cls.mockup_token1_id = mockup_token1.id
        cls.mockup_token2_id = mockup_token2.id

    def test_reseed_token(self):
        mockup_token_id = self.mockup_token1_id

        self.request(As.provider, 'RESEED', f'{self.url}/{mockup_token_id}')

        token = self.session.query(Token).filter(Token.id == mockup_token_id).one_or_none()
        self.assertNotEqual(token.seed, self.mockup_token1_initial_seed)

        # It shouldn't change manually
        self.request(
            As.provider, 'RESEED', f'{self.url}/{mockup_token_id}',
            params=[
                FormParameter(
                    'seed',
                    b'\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06'
                    b'\xab\x0b5\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xf5j\xaaz'
                )
            ],
            expected_status=400
        )

    def test_reseed_uniqueness(self):
        mockup_token_id_1 = self.mockup_token1_id
        mockup_token_id_2 = self.mockup_token2_id

        # Now we want to fix the random method and check reseeding token
        with RandomMonkeyPatch(mockup_seed):
            # Single token
            self.request(As.provider, 'RESEED', f'{self.url}/{mockup_token_id_1}', doc=False)
            self.request(
                As.provider, 'RESEED', f'{self.url}/{mockup_token_id_1}',
                doc=False,
                expected_status=409,
                expected_headers={
                    'x-reason': 'token-initialization-error'
                }
            )

            # Or another token
            self.request(
                As.provider, 'RESEED', f'{self.url}/{mockup_token_id_2}',
                doc=False,
                expected_status=409,
                expected_headers={
                    'x-reason': 'token-initialization-error'
                }
            )


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
