import unittest

from restfulpy.orm import DBSession
from restfulpy.principal import JwtPrincipal
from bddrest.authoring import when, then, response, and_

from wolf.tests.helpers import BDDTestClass
from wolf.models import Admin


class AuthenticationTestCase(BDDTestClass):

    @classmethod
    def mockup(cls):
        admin = Admin()
        admin.username = 'admin'
        admin.password = '123456'
        DBSession.add(admin)
        DBSession.commit()

    def test_login(self):
        call = dict(
            title='Login',
            description='Login to system as admin',
            url='/apiv1/members',
            verb='LOGIN',
            form={
                'username': 'admin',
                'password': '123456',
            }
        )
        with self.given(**call):
            then(response.status_code == 200)
            and_('token' in response.json)
            principal = JwtPrincipal.load(response.json['token'])
            and_('sessionId' in principal.payload)

            when(
                'Trying to login with invalid username and_ password',
                form={
                    'username': 'invalidUserName',
                    'password': 'invalidPassword',
                }
            )
            then(response.status_code == 400)

            when(
                'Trying to login with invalid password',
                form={
                    'username': 'admin',
                    'password': 'invalidPassword',
                }
            )
            then(response.status_code == 400)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
