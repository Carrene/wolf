import unittest
import base64

from bddrest.authoring import when, response, status

from wolf.tests.helpers import LocalApplicationTestCase


class TestAddDevice(LocalApplicationTestCase):

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
            assert status == 200

            result = response.json
            assert 'phone' in result
            assert 'secret' in result
            assert 'createdAt' in result
            assert 'createdAt' in result
            assert result['phone'] == phone
            assert len(base64.decodebytes(result['secret'].encode())) == 32
            first_secret = result['secret']

            when(
                'Trying to registering the same device again',
            )
            assert status == 200
            assert response.json['secret'] != first_secret

