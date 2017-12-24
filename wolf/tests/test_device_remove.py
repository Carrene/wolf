import unittest

from restfulpy.orm import DBSession

from wolf.models.device import Device
from wolf.tests.helpers import WebTestCase, As


# https://github.com/Carrene/wolf/wiki/User-Stories#add-or-remove-device
class RemoveDeviceTestCase(WebTestCase):
    url = '/apiv1/devices'

    @classmethod
    def mockup(cls):
        mockup_device = Device()
        mockup_device.reference_id = 111
        mockup_device.secret = b'\xa1(\x05\xe1\x05\xb9\xc8c\xfb\x89\x87|\xf7"\xf0\xc4h\xe1$=\x81\xc8k\x17rD,p\x1a\xcfT!'

        DBSession.add(mockup_device)
        DBSession.commit()

        cls.mockup_device_reference_id = mockup_device.reference_id

    def test_remove_device(self):

        mockup_device_reference_id = self.mockup_device_reference_id

        result, ___ = self.request(As.device_manager, 'REMOVE', f'{self.url}/{mockup_device_reference_id}')

        self.assertIn('referenceId', result)
        self.assertIn('secret', result)
        self.assertIn('createdAt', result)

        self.assertNotIn('id', result)

        self.assertEqual(result['referenceId'], 111)

        device = self.session.query(Device).filter(Device.reference_id == 111).one_or_none()
        self.assertIsNone(device)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
