import unittest

from restfulpy.orm import DBSession
from bddrest.authoring import when, then, response

from wolf.tests.helpers import BDDTestClass
from wolf.models import Admin


class ChangePasswordTestCase(BDDTestClass):

    @classmethod
    def mockup(cls):
        admin = Admin()
        admin.username = 'admin'
        admin.password = '123456'
        DBSession.add(admin)
        DBSession.commit()
        cls.member_id = admin.id

    def test_change_password(self):
        self.login('admin', '123456')
        call = dict(
            title='Change',
            description='Change Password',
            url=f'/apiv1/members/member_id: {self.member_id}/password',
            verb='CHANGE',
            form={
                'currentPassword': '123456',
                'newPassword': '1234567',
            }
        )

        with self.given(**call):
            then(response.status_code == 200)

            when(
                'Trying to change password with wrong current password',
            )
            then(response.status_code == 400)

            when(
                'Trying to change another user password',
                url_parameters=dict(member_id=999),
            )
            then(response.status_code == 403)

        login_call = dict(
            title='Login',
            description='Try to login to system with old password',
            url='/apiv1/members',
            verb='LOGIN',
            form={
                'username': 'admin',
                'password': '123456',
            }
        )
        with self.given(**login_call):
            then(response.status_code == 400)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
