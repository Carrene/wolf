import unittest

from restfulpy.orm import DBSession
from restfulpy.testing.documentation import FormParameter

from wolf.models import Token, OathCryptomodule
from wolf.tests.helpers import WebTestCase, As


# https://github.com/Carrene/wolf/wiki/User-Stories#extend-token-expiration-time
class ExtendTokenTestCase(WebTestCase):
    url = '/apiv1/tokens'

    @classmethod
    def mockup(cls):
        mockup_token = Token()
        mockup_token.name = 'name1'
        mockup_token.provider_reference = 1
        mockup_token.client_reference = 1
        mockup_token.expire_date = '2009-12-07T18:14:39'
        mockup_token.seed = \
            b'\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5' \
            b'\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xf5j\xaaz'
        mockup_token.is_active = True
        mockup_cryptomodule = OathCryptomodule()
        mockup_token.cryptomodule = mockup_cryptomodule

        DBSession.add(mockup_token)
        DBSession.commit()

        cls.mockup_token_id = mockup_token.id

    def test_extend_token(self):
        mockup_token_id = self.mockup_token_id

        result, ___ = self.request(
            As.provider, 'EXTEND', f'{self.url}/{mockup_token_id}',
            params=[
                FormParameter('expireDate', '2020-12-07')
            ]
        )

        self.assertEqual(result['expireDate'], '2020-12-07')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
