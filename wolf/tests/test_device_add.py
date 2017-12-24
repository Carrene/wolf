import unittest
import base64

from restfulpy.testing.documentation import FormParameter

from wolf.tests.helpers import WebTestCase, As


# https://github.com/Carrene/wolf/wiki/User-Stories#add-or-remove-device
class AddDeviceTestCase(WebTestCase):
    url = '/apiv1/devices'

    def test_add_device(self):

        result, ___ = self.request(
            As.device_manager, 'ADD', self.url,
            params=[
                FormParameter('referenceId', '111', type_=int),
                FormParameter('clientFactor', 'client-phone'),
                FormParameter('deviceFactor', 'device-uid'),
            ]
        )

        self.assertIn('referenceId', result)
        self.assertIn('secret', result)
        self.assertIn('createdAt', result)

        self.assertNotIn('id', result)

        self.assertEqual(result['referenceId'], 111)
        self.assertEqual(len(base64.decodebytes(result['secret'].encode())), 32)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
