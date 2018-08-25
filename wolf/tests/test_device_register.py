import unittest
import base64

from bddrest.authoring import when, then, response, and_

import pyximport; pyximport.install(pyimport=True)
from wolf.tests.helpers import BDDTestClass


# https://github.com/Carrene/wolf/wiki/User-Stories#add-or-remove-device
class AddDeviceTestCase(BDDTestClass):

    def test_register_device(self):
        udid = '2b6f0cc904d137be2e1730235f5664094b831186'
        phone = 989122451075

        call = dict(
            title='Registering a device',
            description='Registering a device by phone and_ udid',
            url='/apiv1/devices',
            verb='REGISTER',
            form={
                'phone': phone,
                'udid': udid,
            }
        )

        with self.given(**call):
            then(response.status_code == 200)
            result = response.json
            and_('phone' in result)
            and_('secret' in result)
            and_('createdAt' in result)
            and_('createdAt' in result)

            and_(result['phone'] == phone)
            and_(len(base64.decodebytes(result['secret'].encode())) == 32)
            first_secret = result['secret']

            when(
                'Trying to registering the same device again',
            )
            then(response.status_code == 200)
            and_(response.json['secret'] != first_secret)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
