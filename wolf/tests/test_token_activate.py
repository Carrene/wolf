import unittest

from nanohttp import settings
from restfulpy.orm import DBSession

from wolf.models import Cryptomodule, Token
from wolf.tests.helpers import BDDTestClass
from bddrest import When, Then, Given, response, And


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
        active_token.consecutive_tries = 0
        active_token.cryptomodule = mockup_cryptomodule
        DBSession.add(active_token)

        deactive_token = Token()
        deactive_token.name = 'deactive_token'
        deactive_token.phone = 989121234567
        deactive_token.expire_date = '2099-12-07T18:14:39.558891'
        deactive_token.seed = b'\xca!\x8e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz'
        deactive_token.is_active = False
        deactive_token.consecutive_tries = settings.token.max_consecutive_tries + 1
        deactive_token.cryptomodule = mockup_cryptomodule
        DBSession.add(deactive_token)

        DBSession.commit()
        cls.mockup_active_token_id = active_token.id
        cls.mockup_deactive_token_id = deactive_token.id
        cls.mockup_cryptomodule_id = mockup_cryptomodule.id

    def test_activate_token(self):
        active_mockup_token_id = self.mockup_active_token_id
        deactive_mockup_token_id = self.mockup_deactive_token_id
        none_existence_token_id = 0

        call = self.call(
            title='Activate a token',
            description='Activate a token by id',
            url=f'/apiv1/tokens/{deactive_mockup_token_id}',
            verb='ACTIVATE',
        )

        with Given(call):
            Then(response.status_code == 200)
            And(response.json['id'] == deactive_mockup_token_id)
            And(response.json['isActive'] is True)

            When(
                'Trying to activate a none existence token',
                url=f'/apiv1/tokens/{none_existence_token_id}',
            )
            Then(response.status_code == 404)

            When(
                'Trying to activate a active token',
                url=f'/apiv1/tokens/{active_mockup_token_id}',
            )
            Then(response.status_code == 409)
            And(self.assertDictEqual(response.json, dict(
                message='Conflict',
                description='Token is already active.'
            )))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
