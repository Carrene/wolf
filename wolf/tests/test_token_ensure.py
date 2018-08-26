import time
import unittest
from datetime import date, timedelta

from nanohttp import settings
from bddrest.authoring import when, response, status

from wolf.models import Cryptomodule, Token, Device
from wolf.tests.helpers import RandomMonkeyPatch, LocalApplicationTestCase


HOUR = 3600
DAY = HOUR * 24


class TestEnsureToken(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        mockup_cryptomodule = Cryptomodule()
        session.add(mockup_cryptomodule)

        expired_token = Token()
        expired_token.name = 'ExpiredToken'
        expired_token.phone = 989122451075
        expired_token.expire_date = date.today() - timedelta(days=1)
        # FIXME: What about only 20 bytes
        expired_token.seed = \
            b'\xdb!\x2e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz' \
            b'\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz' \
            b'\xda!\x9f\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz' \
            b'\xf5j\xaaz'
        expired_token.is_active = True
        expired_token.cryptomodule = mockup_cryptomodule
        session.add(expired_token)

        deactivated_token = Token()
        deactivated_token.name = 'DeactivatedToken'
        deactivated_token.phone = 989122451075
        deactivated_token.expire_date = '2099-12-07T18:14:39.558891'
        deactivated_token.seed = \
            b'\xeb!\x2e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz' \
            b'\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz' \
            b'\xda!\x9f\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz' \
            b'\xf5j\xaaz'
        deactivated_token.is_active = False
        deactivated_token.cryptomodule = mockup_cryptomodule
        session.add(deactivated_token)

        mockup_device = Device()
        mockup_device.phone = 989122451075
        mockup_device.secret = \
            b'\xa1(\x05\xe1\x05\xb9\xc8c\xfb\x89\x87|\xf7"\xf0\xc4h\xe1$=' \
            b'\x81\xc8k\x17rD,p\x1a\xcfT!'
        session.add(mockup_device)

        session.commit()
        cls.mockup_cryptomodule_id = mockup_cryptomodule.id

    def test_ensure_token(self):
        with RandomMonkeyPatch(
            b'F\x8e\x16\xb1w$B\xc7\x01\xa2\xf0\xc4h\xe1\xf7"\xf8\x98w\xcf' \
            b'\x0cF\x8e\x16\xb1t,p\x1a\xcfT!'
        ), self.given(
            'Provisioning',
            '/apiv1/tokens',
            'ENSURE',
            form={
                'phone': 989122451075,
                'name': 'DummyTokenName',
                'cryptomoduleId': self.mockup_cryptomodule_id,
                'expireDate': 1613434403,
            }
        ):

            assert status == 200
            result = response.json
            assert 'provisioning' in result
            assert result['expireDate'] == '2021-02-16'
            token = result['provisioning']
            assert token == \
                'mt://oath/totp/DUMMYTOKENNAME468E16B1772442C701A2F0C468E1F7' \
                '22EC53B78112F9B1AD7C46425A2EAE3371043A34342C84A7CAFCF82298A' \
                '12F3440012102163515'

            when(
                'Ensure the same token again',
                form={
                    'phone': 989122451075,
                    'name': 'DummyTokenName',
                    'cryptomoduleId': self.mockup_cryptomodule_id,
                    'expireDate': 1513434403,
                }
            )
            assert status == 200
            assert 'provisioning' in response.json
            assert response.json['provisioning'] == token

    def test_invalid_cryptomodule_id(self):
        with RandomMonkeyPatch(
            b'F\x8e\x16\xb1w$B\xc7\x01\xa2\xf0\xc4h\xe1\xf7"\xf8\x98w\xcf'
            b'\xcf\x8e\x16\xb1t,p\x1a\xcfT!'
        ), self.given(
            'Provisioning with string',
            '/apiv1/tokens',
            'ENSURE',
            form={
                'phone': 989122451075,
                'name': 'DummyTokenName',
                'cryptomoduleId': 'InvalidCryptomoduleId',
                'expireDate': 1513434403,
            },
        ):
            assert status == '471 cryptomoduleId must be integer'

        with RandomMonkeyPatch(
            b'F\x16\x16\xb1w$B\xc7\x01\xa2\xf0\xc4h\xe1\xf7"\xf8\x98w\xcf'
            b'\xcf\x8e\x16\xb1t,p\x1a\xcfT!'
        ), self.given(
            'Provisioning with zero',
            '/apiv1/tokens',
            'ENSURE',
            form={
                'phone': 989122451075,
                'name': 'DummyTokenName',
                'cryptomoduleId': 0,
                'expireDate': 1513434403,
            },
        ):

            assert status == '472 Invalid cryptomodule id'

    def test_invalid_token_name(self):

        with RandomMonkeyPatch(
            b'F\x9e\x16\xb1w$B\xc7\x01\xa2\xf0\xc4h\xe1\xf7"\xf8\x98w\xcf' \
            b'\xcf\x8e\x16\xb1t,p\x1a\xcfT!'
        ), self.given(
            'Provisioning with empty token name',
            '/apiv1/tokens',
            'ENSURE',
            form={
                'phone': 989122451075,
                'name': '',
                'cryptomoduleId': self.mockup_cryptomodule_id,
                'expireDate': time.time() + DAY,
            },
        ):
            assert status == '471 Token name should at least 16 cahracters'

        with RandomMonkeyPatch(
            b'F\x2e\x16\xb1w$B\xc7\x01\xa2\xf0\xc4h\xe1\xf7"\xf8\x98w\xcf' \
            b'\xcf\x8e\x16\xb1t,p\x1a\xcfT!'
        ), self.given(
            'ensure token with provisioning with a long token name',
            '/apiv1/tokens',
            'ENSURE',
            form={
                'phone': 989122451075,
                'name': f'MoreThan50Chars{"x" * 36}',
                'cryptomoduleId': self.mockup_cryptomodule_id,
                'expireDate': 1513434403,
            },
        ):
            assert status == \
                '472 Token name shouldn\'t be more than 50 cahracters'

    def test_expired_token(self):

        with self.given(
            'Provisioning with an expired token',
            '/apiv1/tokens',
            'ENSURE',
            form={
                'phone': 989122451075,
                'name': 'ExpiredToken',
                'cryptomoduleId': self.mockup_cryptomodule_id,
                'expireDate': 1513434403,
            }
        ):
            assert status == '461 Token is expired'

    def test_deactivated_token(self):

        with self.given(
            'Provisioning with an deactivated token',
            '/apiv1/tokens',
            'ENSURE',
            form={
                'phone': 989122451075,
                'name': 'DeactivatedToken',
                'cryptomoduleId': self.mockup_cryptomodule_id,
                'expireDate': 1513434403,
            }
        ):
            assert status == '463 Token is deactivated'

