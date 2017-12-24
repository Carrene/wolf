import unittest

from restfulpy.orm import DBSession
from restfulpy.testing import FormParameter

from wolf.models import OathCryptomodule
from wolf.tests.helpers import WebTestCase, As


# https://github.com/Carrene/wolf/wiki/User-Stories#edit-crypto-module
class EditOathCryptomoduleTestCase(WebTestCase):
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

    def test_oath_cryptomodule_get(self):
        mockup_cryptomodule_id = self.mockup_cryptomodule_id

        # Change values and check changes
        new_hash_algorithm = 'SHA-512'
        new_counter_type = 'time'
        new_time_interval = 120
        new_one_time_password_length = 4
        new_challenge_response_length = 4

        # We can edit these items:
        # Singular:
        self.request(
            As.provider, 'EDIT', f'{self.url}/{mockup_cryptomodule_id}',
            params=[
                FormParameter('hashAlgorithm', new_hash_algorithm, optional=True),
            ]
        )
        # Or plural:
        result, ___ = self.request(
            As.provider, 'EDIT', f'{self.url}/{mockup_cryptomodule_id}',
            params=[
                FormParameter('counterType', new_counter_type, optional=True),
                FormParameter('timeInterval', new_time_interval, type_=int, optional=True),
                FormParameter('oneTimePasswordLength', new_one_time_password_length, type_=int, optional=True),
                FormParameter('challengeResponseLength', new_challenge_response_length, type_=int, optional=True),
            ]
        )

        self.assertEqual(result['hashAlgorithm'], new_hash_algorithm)
        self.assertEqual(result['counterType'], new_counter_type)
        self.assertEqual(result['timeInterval'], new_time_interval)
        self.assertEqual(result['oneTimePasswordLength'], new_one_time_password_length)
        self.assertEqual(result['challengeResponseLength'], new_challenge_response_length)

        # We can NOT edit these items:
        self.request(
            As.provider, 'EDIT', f'{self.url}/{mockup_cryptomodule_id}',
            params=[
                FormParameter('id', 2),
            ],
            expected_status=400
        )
        self.request(
            As.provider, 'EDIT', f'{self.url}/{mockup_cryptomodule_id}',
            params=[
                FormParameter('providerReference', 2),
            ],
            expected_status=400
        )
        self.request(
            As.provider, 'EDIT', f'{self.url}/{mockup_cryptomodule_id}',
            params=[
                FormParameter('isActive', False),
            ],
            expected_status=400
        )
        self.request(
            As.provider, 'EDIT', f'{self.url}/{mockup_cryptomodule_id}',
            params=[
                FormParameter('createdAt', '2009-12-07T18:14:39.558891'),
            ],
            expected_status=400
        )
        self.request(
            As.provider, 'EDIT', f'{self.url}/{mockup_cryptomodule_id}',
            params=[
                FormParameter('modifiedAt', '2009-12-07T18:14:39.558891'),
            ],
            expected_status=400
        )


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
