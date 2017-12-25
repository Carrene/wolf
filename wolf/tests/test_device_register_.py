import unittest
import base64

from restfulpy.testing.documentation import FormParameter

from wolf.tests.helpers import WebTestCase, As


# https://github.com/Carrene/wolf/wiki/User-Stories#add-or-remove-device
class AddDeviceTestCase(WebTestCase):
    url = '/apiv1/devices'

    def test_register_device(self):
        udid = '2b6f0cc904d137be2e1730235f5664094b831186'
        phone = 989122451075
        result, ___ = self.request(
            As.device_manager, 'REGISTER', self.url,
            params=[
                FormParameter('phone', phone),
                FormParameter('udid', udid),
            ]
        )

        self.assertIn('phone', result)
        self.assertIn('secret', result)
        self.assertIn('createdAt', result)

        self.assertNotIn('id', result)

        self.assertEqual(result['phone'], phone)
        self.assertEqual(len(base64.decodebytes(result['secret'].encode())), 32)
        first_secret = result['secret']

        # Registering the same device again
        result, ___ = self.request(
            As.device_manager, 'REGISTER', self.url,
            params=[
                FormParameter('phone', phone, type_=int),
                FormParameter('udid', udid),
            ]
        )

        self.assertNotEqual(result['secret'], first_secret)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
