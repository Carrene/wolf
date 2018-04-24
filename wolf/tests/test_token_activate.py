import unittest

from nanohttp import settings
from restfulpy.orm import DBSession
from bddrest.authoring import when, then, response, and_

from wolf.models import Cryptomodule, Token
from wolf.tests.helpers import BDDTestClass


class ActivateTokenTestCase(BDDTestClass):

    @classmethod
    def mockup(cls):
        mockup_cryptomodule = Cryptomodule()
        DBSession.add(mockup_cryptomodule)

        active_token = Token()
        active_token.name = 'active_token'
        active_token.phone = 989121234567
        active_token.expire_date = '2000-12-07T18:14:39.558891'
        active_token.seed = b'\xda!\x8e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz'
        active_token.is_active = True
        active_token.cryptomodule = mockup_cryptomodule
        DBSession.add(active_token)

        deactive_token = Token()
        deactive_token.name = 'deactive_token'
        deactive_token.phone = 989121234567
        deactive_token.expire_date = '2099-12-07T18:14:39.558891'
        deactive_token.seed = b'\xca!\x8e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz'
        deactive_token.is_active = False
        deactive_token.cryptomodule = mockup_cryptomodule
        DBSession.add(deactive_token)

        DBSession.commit()
        cls.mockup_active_token_id = active_token.id
        cls.mockup_deactive_token_id = deactive_token.id
        cls.mockup_cryptomodule_id = mockup_cryptomodule.id

    def test_activate_token(self):
        call = dict(
            title='Activate a token',
            description='Activate a token by id',
            url=f'/apiv1/tokens/token_id: {self.mockup_deactive_token_id}',
            verb='ACTIVATE',
        )

        with self.given(**call):
            then(response.status_code == 200)
            and_(response.json['id'] == self.mockup_deactive_token_id)
            and_(response.json['isActive'] is True)

            when(
                'Trying to activate a none existence token',
                url_parameters=dict(token_id=0),
            )
            then(response.status_code == 404)

            when(
                'Trying to activate a active token',
                url_parameters=dict(token_id=self.mockup_active_token_id),
            )
            then(response.status_code == 465)
            and_(self.assertDictEqual(response.json, dict(
                message='Token is active',
                description='Token is already active.'
            )))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
