import unittest

from restfulpy.orm import DBSession

from wolf.models import OathCryptomodule, Token
from wolf.tests.helpers import WebTestCase, As


# https://github.com/Carrene/wolf/wiki/User-Stories#remove-crypto-module
class RemoveOathCryptomoduleTestCase(WebTestCase):
    url = '/apiv1/cryptomodules'
    token_url = '/apiv1/tokens'

    @classmethod
    def mockup(cls):
        free_mockup_cryptomodule = OathCryptomodule()
        DBSession.add(free_mockup_cryptomodule)

        assigned_mockup_cryptomodule = OathCryptomodule()
        assigned_mockup_cryptomodule.provider_reference = 1
        assigned_mockup_cryptomodule.hash_algorithm = 'SHA-1'
        assigned_mockup_cryptomodule.length = 6
        assigned_mockup_cryptomodule.counter_type = 'time'
        assigned_mockup_cryptomodule.time_interval = 60
        assigned_mockup_cryptomodule.one_time_password_length = 4
        assigned_mockup_cryptomodule.challenge_response_length = 6
        assigned_mockup_cryptomodule.is_active = False

        DBSession.add(assigned_mockup_cryptomodule)
        DBSession.flush()

        mockup_token = Token()
        mockup_token.name = 'name1'
        mockup_token.provider_reference = 1
        mockup_token.client_reference = 1
        mockup_token.cryptomodule_id = assigned_mockup_cryptomodule.id
        mockup_token.expire_date = '2099-12-07T18:14:39'
        mockup_token.seed = \
            b'\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5' \
            b'\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xf5j\xaaz'
        mockup_token.is_active = True

        DBSession.add(mockup_token)
        DBSession.commit()

        cls.mockup_token_id = mockup_token.id

        DBSession.add(assigned_mockup_cryptomodule)
        DBSession.commit()

        cls.assigned_cryptomodule_id = assigned_mockup_cryptomodule.id
        cls.free_cryptomodule_id = free_mockup_cryptomodule.id
        cls.mockup_token_id = mockup_token.id

    def test_remove_oath_cryptomodule(self):

        # Removing an assigned module
        error, ___ = self.request(
            As.provider, 'REMOVE', f'{self.url}/{self.assigned_cryptomodule_id}', expected_status=400
        )
        self.assertEqual(
            error,
            {
                'message': 'foreign_key_violation',
                'description': 'ERROR:  update or delete on table "cryptomodule" violates foreign key constraint '
                               '"token_cryptomodule_id_fkey" on table "token"\nDETAIL:  Key (id)=(2) is still '
                               'referenced from table "token".\n'
            }
        )

        # Removing a free module
        self.request(As.provider, 'REMOVE', f'{self.url}/{self.free_cryptomodule_id}')

        # Really was removed?
        self.request(As.provider, 'REMOVE', f'{self.url}/{self.free_cryptomodule_id}', expected_status=404)
        self.request(As.provider, 'GET', f'{self.url}/{self.free_cryptomodule_id}', expected_status=404)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
