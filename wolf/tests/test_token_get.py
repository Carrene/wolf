import unittest

from nanohttp import settings
from restfulpy.orm import DBSession
from bddrest import When, Then, Given, response, And

from wolf.models import Cryptomodule, Token
from wolf.tests.helpers import BDDTestClass


class GetTokenTestCase(BDDTestClass):

    @classmethod
    def mockup(cls):
        mockup_cryptomodule = Cryptomodule()
        DBSession.add(mockup_cryptomodule)

        first_token = Token()
        first_token.name = 'first_token'
        first_token.phone = 989121234567
        first_token.expire_date = '2099-12-07T18:14:39.558891'
        first_token.seed = b'\xda!\x8e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz'

        first_token.is_active = True
        first_token.consecutive_tries = settings.token.max_consecutive_tries + 1
        first_token.cryptomodule = mockup_cryptomodule
        DBSession.add(first_token)

        DBSession.commit()
        cls.mockup_first_token_id = first_token.id
        cls.mockup_cryptomodule_id = mockup_cryptomodule.id

    def test_get_token(self):
        call = self.call(
            title='Get a token',
            description='Get a single token by id',
            url=f'/apiv1/tokens/token_id: {self.mockup_first_token_id}',
            verb='GET',
        )

        with Given(call):
            Then(response.status_code == 200)
            And(response.json['id'] == self.mockup_first_token_id)
            And('isLocked' in response.json)

            When(
                'Trying to get a none existence token',
                url_parameters=dict(token_id=0),
            )
            Then(response.status_code == 404)

            When(
                'Trying to get a token without providing a token_id',
                url=f'/apiv1/tokens',
            )
            Then(response.status_code == 404)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
