import unittest

from restfulpy.orm import DBSession
from restfulpy.testing.documentation import FormParameter

from wolf.models import OathCryptomodule
from wolf.tests.helpers import WebTestCase, As


# https://github.com/Carrene/wolf/wiki/User-Stories#generate-token
class AddTokenTestCase(WebTestCase):
    url = '/apiv1/tokens'

    @classmethod
    def mockup(cls):
        mockup_cryptomodule1 = OathCryptomodule()
        mockup_cryptomodule1.provider_reference = 1
        DBSession.add(mockup_cryptomodule1)
        DBSession.commit()

        cls.mockup_cryptomodule1_id = mockup_cryptomodule1.id

    def test_generate_token(self):
        mockup_cryptomodule1_id = self.mockup_cryptomodule1_id

        result, ___ = self.request(
            As.provider, 'GENERATE', self.url,
            params=[
                FormParameter('name', 'name1'),
                FormParameter('providerReference', '1', type_=int),
                FormParameter('clientReference', '1', type_=int),
                FormParameter('cryptomoduleId', mockup_cryptomodule1_id, type_=int, optional=True),
                FormParameter('expireDate', '2099-12-07', optional=True),
            ]
        )

        self.assertDictContainsSubset(
            result,
            {
                'providerReference': 1,
                'clientReference': 1,
                'name': 'name1',
                'isActive': True,
                'isExpired': False,
                'isLocked': False,
            }
        )

        self.assertIn('id', result)
        self.assertIn('expireDate', result)
        self.assertIn('createdAt', result)
        self.assertIn('modifiedAt', result)

        self.assertDictContainsSubset(
            result['cryptomodule'],
            {
                'id': mockup_cryptomodule1_id,
                'providerReference': 1,
                'hashAlgorithm': 'SHA-1',
                'oneTimePasswordLength': 4,
                'challengeResponseLength': 6,
                'type': 'oath',
                'counterType': 'time',
                'timeInterval': 60,
                'isActive': True,
            }
        )
        self.assertIn('createdAt', result['cryptomodule'])
        self.assertIn('modifiedAt', result['cryptomodule'])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
