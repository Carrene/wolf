import unittest
from datetime import date, timedelta

from nanohttp import settings
from restfulpy.orm import DBSession
from bddrest.authoring import when, then, response, and_

from wolf.models import Cryptomodule, Token, Device
from wolf.tests.helpers import RandomMonkeyPatch, BDDTestClass


# https://github.com/Carrene/wolf/wiki/User-Stories#token-ensure
class EnsureCardTokenTestCase(BDDTestClass):

    @classmethod
    def mockup(cls):
        mockup_cryptomodule = Cryptomodule()
        DBSession.add(mockup_cryptomodule)

        expired_token = Token()
        expired_token.name = '603799ExpiredToken'
        expired_token.phone = 989122451075
        expired_token.expire_date = date.today() - timedelta(days=1)
        expired_token.seed = \
            b'\xdb!\x2e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5' \
            b'\xf8h\xf5j\xaaz\xda!\x9f\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xf5j\xaaz'
        expired_token.is_active = True
        expired_token.cryptomodule = mockup_cryptomodule
        DBSession.add(expired_token)

        deactivated_token = Token()
        deactivated_token.name = '603799DeactivatedToken'
        deactivated_token.phone = 989122451075
        deactivated_token.expire_date = '2099-12-07T18:14:39.558891'
        deactivated_token.seed = \
            b'\xeb!\x2e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5' \
            b'\xf8h\xf5j\xaaz\xda!\x9f\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xf5j\xaaz'
        deactivated_token.is_active = False
        deactivated_token.cryptomodule = mockup_cryptomodule
        DBSession.add(deactivated_token)

        mockup_device = Device()
        mockup_device.phone = 989122451075
        mockup_device.secret = b'\xa1(\x05\xe1\x05\xb9\xc8c\xfb\x89\x87|\xf7"\xf0\xc4h\xe1$=\x81\xc8k\x17rD,p\x1a\xcfT!'
        DBSession.add(mockup_device)

        DBSession.commit()
        cls.mockup_cryptomodule_id = mockup_cryptomodule.id

    def test_ensure_cardtoken(self):
        call = dict(
            title='Provisioning',
            description='Provisioning',
            url='/apiv1/cardtokens',
            verb='ENSURE',
            form={
                'phone': 989122451075,
                'partialCardName': '603799DummyTokenName',
                'cryptomoduleId': self.mockup_cryptomodule_id,
                'expireDate': 1613434403,
                'bankId': 1,
            }
        )
        with RandomMonkeyPatch(
                b'F\x8e\x16\xb1w$B\xc7\x01\xa2\xf0\xc4h\xe1\xf7"\xf8\x98w\xcf\x0cF\x8e\x16\xb1t,p\x1a\xcfT!'
        ), self.given(**call):

            then(response.status_code == 200)
            result = response.json
            and_('provisioning' in result)
            and_(result['expireDate'] == '2021-02-16')
            token = result['provisioning']
            and_(token == 'mt://oath/totp/603799DUMMYTOKENNAME468E16B1772'
                 '442C701A2F0C468E1F722EC53B78112F9B1AD7C46425A2EAE337104'
                 '3A34342C84A7CAFCF82298A12F3440012102161048')

            when(
                'Invalid bank id type',
                form={
                    'phone': 989122451075,
                    'partialCardName': '603799DummyTokenName',
                    'cryptomoduleId': self.mockup_cryptomodule_id,
                    'expireDate': 1513434403,
                    'bankId': 'not-integer',
                }
            )
            then(response.status_code == 400)

        call = dict(
            title='Provisioning',
            description='Ensure the same token again',
            url='/apiv1/cardtokens',
            verb='ENSURE',
            form={
                'phone': 989122451075,
                'partialCardName': '603799DummyTokenName',
                'cryptomoduleId': self.mockup_cryptomodule_id,
                'expireDate': 1613434403,
                'bankId': 1,
            }
        )

        with self.given(**call):
            then(response.status_code == 200)
            result = response.json
            and_('provisioning' in result)
            and_(result['expireDate'] == '2021-02-16')
            token = result['provisioning']

    def test_invalid_cryptomodule_id(self):
        call = dict(
            title='Provisioning with string',
            description='Provisioning with non-digit cryptomodule id',
            url='/apiv1/cardtokens',
            verb='ENSURE',
            form={
                'phone': 989122451075,
                'partialCardName': '603799DummyTokenName',
                'cryptomoduleId': 'InvalidCryptomoduleId',
                'expireDate': 1513434403,
                'bankId': 1,
            },
        )
        with RandomMonkeyPatch(
                b'F\x8e\x16\xb1w$B\xc7\x01\xa2\xf0\xc4h\xe1\xf7"\xf8\x98w\xcf\xcf\x8e\x16\xb1t,p\x1a\xcfT!'
        ), self.given(**call):

            then(response.status_code == 400)
            and_(self.assertDictEqual(response.json, dict(
                message='Bad Request',
                description='The field: cryptomoduleId must be int'
            )))

        call = dict(
            title='Provisioning with zero',
            description='Trying to ensure token with provisioning with zero cryptomodule id',
            url='/apiv1/cardtokens',
            verb='ENSURE',
            form={
                'phone': 989122451075,
                'partialCardName': '603799DummyTokenName',
                'cryptomoduleId': 0,
                'expireDate': 1513434403,
                'bankId': 1,
            },
        )

        with RandomMonkeyPatch(
                b'F\x16\x16\xb1w$B\xc7\x01\xa2\xf0\xc4h\xe1\xf7"\xf8\x98w\xcf\xcf\x8e\x16\xb1t,p\x1a\xcfT!'
        ), self.given(**call):

            then(response.status_code == 400)
            and_(self.assertDictEqual(response.json, dict(
                message='Bad Request',
                description='Invalid cryptomodule id.'
            )))

    def test_invalid_token_name(self):

        call = dict(
            title='Provisioning with empty token name',
            description='Provisioning with empty token name',
            url='/apiv1/cardtokens',
            verb='ENSURE',
            form={
                'phone': 989122451075,
                'partialCardName': 'InvalidTokenName',
                'cryptomoduleId': self.mockup_cryptomodule_id,
                'expireDate': 1513434403,
                'bankId': 1,
            },
        )

        with RandomMonkeyPatch(
            b'F\x9e\x16\xb1w$B\xc7\x01\xa2\xf0\xc4h\xe1\xf7"\xf8\x98w\xcf\xcf\x8e\x16\xb1t,p\x1a\xcfT!'
        ), self.given(**call):
            then(response.status_code == 400)
            and_(self.assertDictEqual(response.json, dict(
                message='Bad Request',
                description='Invalid partial card name.'
            )))

        call = dict(
            title='ensure token with provisioning with a long token name',
            description='Trying to ensure token with provisioning with a long token name',
            url='/apiv1/cardtokens',
            verb='ENSURE',
            form={
                'phone': 989122451075,
                'partialCardName': f'603799MoreThan50Chars{"x" * 36}',
                'cryptomoduleId': self.mockup_cryptomodule_id,
                'expireDate': 1513434403,
                'bankId': 1,
            },
        )

        with RandomMonkeyPatch(
            b'F\x2e\x16\xb1w$B\xc7\x01\xa2\xf0\xc4h\xe1\xf7"\xf8\x98w\xcf\xcf\x8e\x16\xb1t,p\x1a\xcfT!'
        ), self.given(**call):

            then(response.status_code == 400)
            and_(self.assertDictEqual(response.json, dict(
                message='Bad Request',
                description='Cannot enter more than: 50 in field: partial card name.'
            )))



    def test_expired_token(self):
        call = dict(
            title='Provisioning with an expired token',
            description='Provisioning with an expired token',
            url='/apiv1/cardtokens',
            verb='ENSURE',
            form={
                'phone': 989122451075,
                'partialCardName': '603799ExpiredToken',
                'cryptomoduleId': self.mockup_cryptomodule_id,
                'expireDate': 1513434403,
                'bankId': 1,
            },
        )

        with self.given(**call):
            then(response.status_code == 461)
            and_(self.assertDictEqual(response.json, dict(
                message='Token is expired',
                description='The requested token is expired.'
            )))

    def test_deactivated_token(self):
        call = dict(
            title='Provisioning with an deactivated token',
            description='Provisioning with an deactivated token',
            url='/apiv1/cardtokens',
            verb='ENSURE',
            form={
                'phone': 989122451075,
                'partialCardName': '603799DeactivatedToken',
                'cryptomoduleId': self.mockup_cryptomodule_id,
                'expireDate': 1513434403,
                'bankId': 1,
            },
        )

        with self.given(**call):
            then(response.status_code == 463)
            and_(self.assertDictEqual(response.json, dict(
                message='Token is deactivated',
                description='Token has been deactivated.'
            )))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
