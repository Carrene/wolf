import unittest
import binascii

from Crypto.Cipher import AES
from restfulpy.orm import DBSession
from restfulpy.testing.documentation import FormParameter

from wolf.models import Token, OathCryptomodule
from wolf.models.device import Device
from wolf.tests.helpers import WebTestCase, As, RandomMonkeyPatch
from oathpy import totp_checksum


# https://github.com/Carrene/wolf/wiki/User-Stories#token-provisioning
class ProvisionTokenTestCase(WebTestCase):
    url = '/apiv1/tokens'

    @classmethod
    def mockup(cls):
        mockup_token = Token()
        mockup_token.name = '14--characters'
        mockup_token.provider_reference = 1
        mockup_token.client_reference = 1
        mockup_token.expire_date = '2009-12-07T18:14:39'
        mockup_token.seed = \
            b'\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5' \
            b'\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xf5j\xaaz'

        mockup_token.is_active = True

        mockup_cryptomodule = OathCryptomodule()
        mockup_cryptomodule.provider_reference = 1
        mockup_cryptomodule.hash_algorithm = 'SHA-1'
        mockup_cryptomodule.counter_type = 'time'
        mockup_cryptomodule.time_interval = 60
        mockup_cryptomodule.one_time_password_length = 4
        mockup_cryptomodule.challenge_response_length = 6
        mockup_cryptomodule.is_active = True

        mockup_token.cryptomodule = mockup_cryptomodule

        mockup_device = Device()
        mockup_device.reference_id = 111
        mockup_device.secret = b'\xa1(\x05\xe1\x05\xb9\xc8c\xfb\x89\x87|\xf7"\xf0\xc4h\xe1$=\x81\xc8k\x17rD,p\x1a\xcfT!'

        DBSession.add(mockup_token)
        DBSession.add(mockup_cryptomodule)
        DBSession.add(mockup_device)
        DBSession.commit()

        cls.mockup_token_id = mockup_token.id
        cls.mockup_device_reference_id = mockup_device.reference_id
        cls.mockup_device_secret = mockup_device.secret

        cls.fake_random = b'F\x8e\x16\xb1w$B\xc7\x01\xa2\xf0\xc4h\xe1\xf7"\xf8\x98w\xcf\x0cF\x8e\x16\xb1t,p\x1a\xcfT!'

    def test_provision_token(self):
        mockup_device_reference_id = self.mockup_device_reference_id
        mockup_token_id = self.mockup_token_id

        with RandomMonkeyPatch(self.fake_random):
            result, ___ = self.request(
                As.provider, 'PROVISION', f'{self.url}/{mockup_token_id}',
                params=[
                    FormParameter('deviceReferenceId', mockup_device_reference_id, type_=int)
                ]
            )

            self.assertIn('provisioning', result)
            token = result['provisioning']

            self.assertEqual(
                token,
                'mt://oath/totp/14--characters468e16b1772442c701a2f0c468e1f72258ff381ac3d645f9d89e4e2cc7428b7a44fea7d1'
                'e951960b4a3997d00731852a010912076070'
            )

            self.assertEqual(15+14+96+2+6+4, len(token))

            encrypted_seed = binascii.unhexlify(token[29:125])

            iv = encrypted_seed[:16]
            cipher = AES.new(self.mockup_device_secret, AES.MODE_CBC, iv)
            seed = cipher.decrypt(encrypted_seed[16:])

            self.assertEqual(
                seed,
                b'\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c'
                b'\x0c\x0c'
            )

            # Validating the checksum
            self.assertEqual(totp_checksum(token[15:-4].encode()), token[-4:])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
