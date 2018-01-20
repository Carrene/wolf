import unittest
import base64


from wolf.tests.helpers import DocumentaryTestCase


# https://github.com/Carrene/wolf/wiki/User-Stories#add-or-remove-device
class AddDeviceTestCase(DocumentaryTestCase):

    def test_register_device(self):
        udid = '2b6f0cc904d137be2e1730235f5664094b831186'
        phone = 989122451075
        response = self.call_as_device_manager(
            'Registering a device',
            'REGISTER',
            '/apiv1/devices',
            form={
                'phone': phone,
                'udid': udid,
            }
        )
        result = response.json

        self.assertIn('phone', result)
        self.assertIn('secret', result)
        self.assertIn('createdAt', result)

        self.assertNotIn('id', result)

        self.assertEqual(result['phone'], phone)
        self.assertEqual(len(base64.decodebytes(result['secret'].encode())), 32)
        first_secret = result['secret']

        # Registering the same device again
        response = self.call_as_device_manager(
            'Registering a device twice',
            'REGISTER',
            '/apiv1/devices',
            form={
                'phone': phone,
                'udid': udid
            },
            description='In this case the device secret will be re-randomized and therefore the previous instance of '
                        'the mobile app is not usable anymore'
        )

        self.assertNotEqual(response.json['secret'], first_secret)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
