import unittest

from restfulpy.orm import DBSession

from wolf.models import Token, OathCryptomodule
from wolf.tests.helpers import WebTestCase, As


# https://github.com/Carrene/wolf/wiki/User-Stories#get-token
class GetTokenTestCase(WebTestCase):
    url = '/apiv1/tokens'

    @classmethod
    def mockup(cls):
        mockup_token = Token()
        mockup_token.name = 'name1'
        mockup_token.provider_reference = 1
        mockup_token.client_reference = 1
        mockup_token.expire_date = '2099-12-07T18:14:39.558891'
        mockup_token.seed = \
            b'\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5' \
            b'\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xf5j\xaaz'
        mockup_token.is_active = True
        mockup_cryptomodule = OathCryptomodule()
        mockup_token.cryptomodule = mockup_cryptomodule
        DBSession.add(mockup_token)
        DBSession.commit()

        cls.mockup_token_id = mockup_token.id

    def test_get_token(self):
        mockup_token_id = self.mockup_token_id

        result, ___ = self.request(As.provider, 'GET', f'{self.url}/{mockup_token_id}')

        self.assertDictContainsSubset(
            result,
            {
                'id': mockup_token_id,
                'providerReference': 1,
                'clientReference': 1,
                'name': 'name1',
                'isActive': True,
                'isExpired': False,
                'isLocked': False
            }
        )

        self.assertIn('expireDate', result)
        self.assertIn('createdAt', result)
        self.assertIn('modifiedAt', result)

    def test_get_token_list(self):
        result, ___ = self.request(As.provider, 'GET', self.url)

        self.assertEqual(len(result), 1)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
