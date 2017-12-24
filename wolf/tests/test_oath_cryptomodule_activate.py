import unittest

from restfulpy.orm import DBSession

from wolf.models import OathCryptomodule
from wolf.tests.helpers import WebTestCase, As


# https://github.com/Carrene/wolf/wiki/User-Stories#activate-or-deactivate-crypto-module
class ActivateOathCryptomoduleTestCase(WebTestCase):
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
        mockup_cryptomodule.is_active = False

        DBSession.add(mockup_cryptomodule)
        DBSession.commit()

        cls.mockup_cryptomodule_id = mockup_cryptomodule.id

    def test_activate_oath_cryptomodule(self):
        mockup_cryptomodule_id = self.mockup_cryptomodule_id

        result, ___ = self.request(As.provider, 'ACTIVATE', f'{self.url}/{mockup_cryptomodule_id}')
        self.assertTrue(result['isActive'])

        result, ___ = self.request(As.provider, 'DEACTIVATE', f'{self.url}/{mockup_cryptomodule_id}')
        self.assertFalse(result['isActive'])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
