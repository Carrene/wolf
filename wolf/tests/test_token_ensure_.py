import unittest
from datetime import date, timedelta

from nanohttp import settings
from restfulpy.orm import DBSession

from wolf.models import Cryptomodule, Token, Device
from wolf.tests.helpers import DocumentaryTestCase, RandomMonkeyPatch


# https://github.com/Carrene/wolf/wiki/User-Stories#token-ensure
class EnsureTokenTestCase(DocumentaryTestCase):

    @classmethod
    def mockup(cls):
        mockup_cryptomodule = Cryptomodule()
        DBSession.add(mockup_cryptomodule)

        locked_token = Token()
        locked_token.name = 'LockedToken'
        locked_token.phone = 989122451075
        locked_token.expire_date = '2099-12-07T18:14:39.558891'
        locked_token.seed = \
            b'\xda!\x8e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5' \
            b'\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xf5j\xaaz'
        locked_token.is_active = True
        locked_token.consecutive_tries = settings.token.max_consecutive_tries + 1
        locked_token.cryptomodule = mockup_cryptomodule
        DBSession.add(locked_token)

        expired_token = Token()
        expired_token.name = 'ExpiredToken'
        expired_token.phone = 989122451075
        expired_token.expire_date = date.today() - timedelta(days=1)
        expired_token.seed = \
            b'\xdb!\x2e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5' \
            b'\xf8h\xf5j\xaaz\xda!\x9f\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xf5j\xaaz'
        expired_token.is_active = True
        expired_token.cryptomodule = mockup_cryptomodule
        DBSession.add(expired_token)

        mockup_device = Device()
        mockup_device.phone = 989122451075
        mockup_device.secret = b'\xa1(\x05\xe1\x05\xb9\xc8c\xfb\x89\x87|\xf7"\xf0\xc4h\xe1$=\x81\xc8k\x17rD,p\x1a\xcfT!'
        DBSession.add(mockup_device)

        DBSession.commit()
        cls.mockup_cryptomodule_id = mockup_cryptomodule.id

    def test_ensure_token(self):
        with RandomMonkeyPatch(
            b'F\x8e\x16\xb1w$B\xc7\x01\xa2\xf0\xc4h\xe1\xf7"\xf8\x98w\xcf\x0cF\x8e\x16\xb1t,p\x1a\xcfT!'
        ):
            response = self.call_as_bank(
                'Provisioning',
                'ENSURE',
                '/apiv1/tokens',
                form={
                    'phone': 989122451075,
                    'name': 'DummyTokenName',
                    'cryptomoduleId': self.mockup_cryptomodule_id,
                    'expireDate': 1613434403,
                }
            )

            result = response.json
            self.assertIn('provisioning', result)
            self.assertEqual('2021-02-16', result['expireDate'])
            token = result['provisioning']

            self.assertEqual(
                token,
                'mt://oath/totp/DUMMYTOKENNAME468E16B1772442C701A2F0C468E1F722EC53B78112F9B1AD7C46425A2EAE3371043A343'
                '42C84A7CAFCF82298A12F3440012102163515'
            )

            # Ensure the same token again
            response = self.call_as_bank(
                'Provisioning multiple times',
                'ENSURE',
                '/apiv1/tokens',
                form={
                    'phone': 989122451075,
                    'name': 'DummyTokenName',
                    'cryptomoduleId': self.mockup_cryptomodule_id,
                    'expireDate': 1513434403,
                }
            )

            result = response.json
            self.assertIn('provisioning', result)
            token = result['provisioning']

            self.assertEqual(token, token)

    def test_invalid_cryptomodule_id(self):
        with RandomMonkeyPatch(
            b'F\x8e\x16\xb1w$B\xc7\x01\xa2\xf0\xc4h\xe1\xf7"\xf8\x98w\xcf\xcf\x8e\x16\xb1t,p\x1a\xcfT!'
        ):
            # With string !
            response = self.call_as_bank(
                'Provisioning with non-digit cryptomodule id',
                'ENSURE',
                '/apiv1/tokens',
                form={
                    'phone': 989122451075,
                    'name': 'DummyTokenName',
                    'cryptomoduleId': 'InvalidCryptomoduleId',
                    'expireDate': 1513434403,
                },
                status=400
            )
            self.assertDictEqual(
                response.json,
                {
                    'message': 'Bad Request',
                    'description': 'The field: cryptomoduleId must be int'
                }
            )

        with RandomMonkeyPatch(
                b'F\x16\x16\xb1w$B\xc7\x01\xa2\xf0\xc4h\xe1\xf7"\xf8\x98w\xcf\xcf\x8e\x16\xb1t,p\x1a\xcfT!'
        ):

            # Invalid integer id
            response = self.call_as_bank(
                'Provisioning with zero cryptomodule id',
                'ENSURE',
                '/apiv1/tokens',
                form={
                    'phone': 989122451075,
                    'name': 'DummyTokenName',
                    'cryptomoduleId': 0,
                    'expireDate': 1513434403,
                },
                status=400
            )
            self.assertDictEqual(
                response.json,
                {
                    'message': 'Bad Request',
                    'description': 'Invalid cryptomodule id.'
                }
            )

    def test_invalid_token_name(self):
        # With empty string !
        with RandomMonkeyPatch(
            b'F\x9e\x16\xb1w$B\xc7\x01\xa2\xf0\xc4h\xe1\xf7"\xf8\x98w\xcf\xcf\x8e\x16\xb1t,p\x1a\xcfT!'
        ):
            response = self.call_as_bank(
                'Provisioning with empty token name',
                'ENSURE',
                '/apiv1/tokens',
                form={
                    'phone': 989122451075,
                    'name': '',
                    'cryptomoduleId': self.mockup_cryptomodule_id,
                    'expireDate': 1513434403,
                },
                status=400
            )
            self.assertDictEqual(
                response.json,
                {
                    'message': 'Bad Request',
                    'description': 'Please enter at least 1 characters for field: name.'
                }
            )

        # With max length limit
        with RandomMonkeyPatch(
            b'F\x2e\x16\xb1w$B\xc7\x01\xa2\xf0\xc4h\xe1\xf7"\xf8\x98w\xcf\xcf\x8e\x16\xb1t,p\x1a\xcfT!'
        ):
            response = self.call_as_bank(
                'Provisioning with a long token name',
                'ENSURE',
                '/apiv1/tokens',
                form={
                    'phone': 989122451075,
                    'name': f'MoreThan50Chars{"x" * 36}',
                    'cryptomoduleId': self.mockup_cryptomodule_id,
                    'expireDate': 1513434403,
                },
                status=400
            )
            self.assertDictEqual(
                response.json,
                {
                    'message': 'Bad Request',
                    'description': 'Cannot enter more than: 50 in field: name.'
                }
            )

    def test_locked_token(self):
        with RandomMonkeyPatch(
            b'F\x7e\x16\xb1w$B\xc7\x01\xa2\xf0\xc4h\xe1\xf7"\xf8\x98w\xcf\x0cF\x8e\x16\xb1t,p\x1a\xcfT!'
        ):
            # Ensure the same token again
            response = self.call_as_bank(
                'Provisioning with a locked token',
                'ENSURE',
                '/apiv1/tokens',
                form={
                    'phone': 989122451075,
                    'name': 'LockedToken',
                    'cryptomoduleId': self.mockup_cryptomodule_id,
                    'expireDate': 1513434403,
                },
                status=462
            )
            self.assertDictEqual(
                response.json,
                {
                    'message': 'Token is locked',
                    'description': 'The max try limitation is exceeded.'
                }
            )

    def test_expired_token(self):
        # Ensure the same token again
        response = self.call_as_bank(
            'Provisioning with an expired token',
            'ENSURE',
            '/apiv1/tokens',
            form={
                'phone': 989122451075,
                'name': 'ExpiredToken',
                'cryptomoduleId': self.mockup_cryptomodule_id,
                'expireDate': 1513434403,
            },
            status=461
        )
        self.assertDictEqual(
            response.json,
            {
                'message': 'Token is expired',
                'description': 'The requested token is expired.'
            }
        )


if __name__ == '__main__':  # pragma: no cover
    unittest.main()