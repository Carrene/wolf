import unittest
import base64

from wolf.tests.helpers import BDDTestClass
from bddrest import When, Then, Given, response, And


# https://github.com/Carrene/wolf/wiki/User-Stories#add-or-remove-device
class AddDeviceTestCase(BDDTestClass):

    def test_register_device(self):
        udid = '2b6f0cc904d137be2e1730235f5664094b831186'
        phone = 989122451075

        call = self.call(
            title='Registering a device',
            description='Registering a device by phone and udid',
            url='/apiv1/devices',
            verb='REGISTER',
            form={
                'phone': phone,
                'udid': udid,
            }
        )

        with Given(call):
            Then(response.status_code == 200)
            result = response.json
            And('phone' in result)
            And('secret' in result)
            And('createdAt' in result)
            And('createdAt' in result)

            And(result['phone'] == phone)
            And(len(base64.decodebytes(result['secret'].encode())) == 32)
            first_secret = result['secret']

            When(
                'Trying to registering the same device again',
            )
            Then(response.status_code == 200)
            And(response.json['secret'] != first_secret)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
