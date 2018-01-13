import unittest

from restfulpy.orm import DBSession
from restfulpy.principal import JwtPrincipal
from bddrest import When, Then, Given, response, And

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
        call = self.call(
            title='Login',
            description='Login to system as admin',
            url='/apiv1/members',
            verb='LOGIN',
            form={
                'username': 'admin',
                'password': '123456',
            }
        )
        with Given(call):
            Then(response.status_code == 200)
            And('token' in response.json)
            principal = JwtPrincipal.load(response.json['token'])
            And('sessionId' in principal.payload)

            When(
                'Trying to login with invalid username and password',
                form={
                    'username': 'invalidUserName',
                    'password': 'invalidPassword',
                }
            )
            Then(response.status_code == 400)

            When(
                'Trying to login with invalid password',
                form={
                    'username': 'admin',
                    'password': 'invalidPassword',
                }
            )
            Then(response.status_code == 400)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
