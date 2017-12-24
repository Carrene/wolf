import unittest

from restfulpy.orm import DBSession

from wolf.models import OathCryptomodule
from wolf.tests.helpers import WebTestCase, As


# https://github.com/Carrene/wolf/wiki/User-Stories#get-crypto-module
class GetOathCryptomoduleTestCase(WebTestCase):
    url = '/apiv1/cryptomodules'

    @classmethod
    def mockup(cls):
        mockup_cryptomodule = OathCryptomodule()
        mockup_cryptomodule.provider_reference = 1
        mockup_cryptomodule.hash_algorithm = 'SHA-1'
        mockup_cryptomodule.counter_type = 'time'
        mockup_cryptomodule.time_interval = 60
        mockup_cryptomodule.one_time_password_length = 4
        mockup_cryptomodule.challenge_response_length = 6
        mockup_cryptomodule.is_active = True

        DBSession.add(mockup_cryptomodule)
        DBSession.commit()

        cls.mockup_cryptomodule_id = mockup_cryptomodule.id

    def test_get_oath_cryptomodule(self):
        mockup_cryptomodule_id = self.mockup_cryptomodule_id

        result, ___ = self.request(As.provider, 'GET', f'{self.url}/{mockup_cryptomodule_id}')

        self.assertDictContainsSubset(
            result,
            {
                'id': mockup_cryptomodule_id,
                'providerReference': 1,
                'hashAlgorithm': 'SHA-1',
                'counterType': 'time',
                'timeInterval': 60,
                'oneTimePasswordLength': 4,
                'challengeResponseLength': 6,
                'type': 'oath',
                'isActive': True,
            }
        )

        self.assertIn('createdAt', result)
        self.assertIn('modifiedAt', result)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
