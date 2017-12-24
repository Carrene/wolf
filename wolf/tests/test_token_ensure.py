import unittest

from nanohttp import settings
from restfulpy.orm import DBSession
from restfulpy.testing.documentation import FormParameter

from wolf.models import Cryptomodule, Token, Device
from wolf.tests.helpers import WebTestCase, As, RandomMonkeyPatch


# https://github.com/Carrene/wolf/wiki/User-Stories#token-ensure
class EnsureTokenTestCase(WebTestCase):
    url = '/apiv1/tokens'

    @classmethod
    def mockup(cls):
        mockup_cryptomodule = Cryptomodule()
        DBSession.add(mockup_cryptomodule)

        locked_token = Token()
        locked_token.name = 'LockedToken'
        locked_token.client_reference = 989122451075
        locked_token.expire_date = '2099-12-07T18:14:39.558891'
        locked_token.seed = \
            b'\xda!\x8e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5' \
            b'\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xf5j\xaaz'
        locked_token.is_active = True
        locked_token.consecutive_tries = settings.token.max_consecutive_tries + 1
        locked_token.cryptomodule = mockup_cryptomodule
        DBSession.add(locked_token)

        mockup_device = Device()
        mockup_device.reference_id = 989122451075
        mockup_device.secret = b'\xa1(\x05\xe1\x05\xb9\xc8c\xfb\x89\x87|\xf7"\xf0\xc4h\xe1$=\x81\xc8k\x17rD,p\x1a\xcfT!'
        DBSession.add(mockup_device)

        DBSession.commit()
        cls.mockup_cryptomodule_id = mockup_cryptomodule.id

    def test_ensure_token(self):
        with RandomMonkeyPatch(
            b'F\x8e\x16\xb1w$B\xc7\x01\xa2\xf0\xc4h\xe1\xf7"\xf8\x98w\xcf\x0cF\x8e\x16\xb1t,p\x1a\xcfT!'
        ):
            result, ___ = self.request(
                As.provider, 'ENSURE', self.url,
                params=[
                    FormParameter('clientReference', 989122451075, type_=int),
                    FormParameter('name', 'DummyTokenName'),
                    FormParameter('cryptomoduleId', self.mockup_cryptomodule_id, type_=int),
                    FormParameter('expireDate', '1513434403', type_='date'),
                ]
            )

            self.assertIn('provisioning', result)
            token = result['provisioning']

            self.assertEqual(
                token,
                'mt://oath/totp/DUMMYTOKENNAME468E16B1772442C701A2F0C468E1F722EC53B78112F9B1AD7C46425A2EAE3371043A343'
                '42C84A7CAFCF82298A12F3440011712165311'
            )

            # Ensure the same token again
            result, ___ = self.request(
                As.provider, 'ENSURE', self.url,
                params=[
                    FormParameter('clientReference', 989122451075, type_=int),
                    FormParameter('name', 'DummyTokenName'),
                    FormParameter('cryptomoduleId', self.mockup_cryptomodule_id, type_=int),
                    FormParameter('expireDate', '1513434403', type_='date'),
                ]
            )

            self.assertIn('provisioning', result)
            token = result['provisioning']

            self.assertEqual(
                token,
                'mt://oath/totp/DUMMYTOKENNAME468E16B1772442C701A2F0C468E1F722EC53B78112F9B1AD7C46425A2EAE3371043A343'
                '42C84A7CAFCF82298A12F3440011712165311'
            )

    def test_invalid_cryptomodule_id(self):
        with RandomMonkeyPatch(
            b'F\x8e\x16\xb1w$B\xc7\x01\xa2\xf0\xc4h\xe1\xf7"\xf8\x98w\xcf\xcf\x8e\x16\xb1t,p\x1a\xcfT!'
        ):
            # With string !
            error, ___ = self.request(
                As.provider, 'ENSURE', self.url,
                params=[
                    FormParameter('clientReference', 989122451075, type_=int),
                    FormParameter('name', 'DummyTokenName'),
                    FormParameter('cryptomoduleId', 'InvalidCryptomoduleId', type_=int),
                    FormParameter('expireDate', '1513434403', type_='date'),
                ],
                expected_status=400
            )
            self.assertDictEqual(
                error,
                {
                    'message': 'Bad Request',
                    'description': 'The field: cryptomoduleId must be int'
                }
            )

        with RandomMonkeyPatch(
                b'F\x16\x16\xb1w$B\xc7\x01\xa2\xf0\xc4h\xe1\xf7"\xf8\x98w\xcf\xcf\x8e\x16\xb1t,p\x1a\xcfT!'
        ):

            # Invalid integer id
            error, ___ = self.request(
                As.provider, 'ENSURE', self.url,
                params=[
                    FormParameter('clientReference', 989122451075, type_=int),
                    FormParameter('name', 'DummyTokenName'),
                    FormParameter('cryptomoduleId', 0, type_=int),
                    FormParameter('expireDate', '1513434403', type_='date'),
                ],
                expected_status=400
            )

            self.assertDictEqual(
                error,
                {
                    'message': 'foreign_key_violation',
                    'description': 'ERROR:  insert or update on table "token" violates foreign key constraint "token_'
                                   'cryptomodule_id_fkey"\nDETAIL:  Key (cryptomodule_id)=(0) is not present in table '
                                   '"cryptomodule".\n'
                })

    def test_invalid_token_name(self):
        # With empty string !
        with RandomMonkeyPatch(
            b'F\x9e\x16\xb1w$B\xc7\x01\xa2\xf0\xc4h\xe1\xf7"\xf8\x98w\xcf\xcf\x8e\x16\xb1t,p\x1a\xcfT!'
        ):
            error, ___ = self.request(
                As.provider, 'ENSURE', self.url,
                params=[
                    FormParameter('clientReference', 989122451075, type_=int),
                    FormParameter('name', ''),
                    FormParameter('cryptomoduleId', self.mockup_cryptomodule_id, type_=int),
                    FormParameter('expireDate', '1513434403', type_='date'),
                ],
                expected_status=400
            )
            self.assertDictEqual(
                error,
                {
                    'message': 'Bad Request',
                    'description': 'Please enter at least 1 characters for field: name.'
                }
            )

        # With max length limit
        with RandomMonkeyPatch(
            b'F\x2e\x16\xb1w$B\xc7\x01\xa2\xf0\xc4h\xe1\xf7"\xf8\x98w\xcf\xcf\x8e\x16\xb1t,p\x1a\xcfT!'
        ):
            error, ___ = self.request(
                As.provider, 'ENSURE', self.url,
                params=[
                    FormParameter('clientReference', 989122451075, type_=int),
                    FormParameter('name', f'MoreThan50Chars{"x" * 36}'),
                    FormParameter('cryptomoduleId', self.mockup_cryptomodule_id, type_=int),
                    FormParameter('expireDate', '1513434403', type_='date'),
                ],
                expected_status=400
            )
            self.assertDictEqual(
                error,
                {
                    'message': 'Bad Request',
                    'description': 'Cannot enter more than: 50 in field: name.'
                }
            )

    def test_locked_token(self):
        # Creating a fresh token to lock it
        with RandomMonkeyPatch(
            b'F\x7e\x16\xb1w$B\xc7\x01\xa2\xf0\xc4h\xe1\xf7"\xf8\x98w\xcf\x0cF\x8e\x16\xb1t,p\x1a\xcfT!'
        ):
            # Ensure the same token again
            error, ___ = self.request(
                As.provider, 'ENSURE', self.url,
                params=[
                    FormParameter('clientReference', 989122451075, type_=int),
                    FormParameter('name', 'LockedToken'),
                    FormParameter('cryptomoduleId', self.mockup_cryptomodule_id, type_=int),
                    FormParameter('expireDate', '1513434403', type_='date'),
                ],
                expected_status=462
            )

            self.assertDictEqual(
                error,
                {
                    'message': 'Token is locked',
                    'description': 'The max try limitation is exceeded.'
                }
            )


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
