import unittest
from datetime import date, timedelta

from nanohttp import settings
from restfulpy.orm import DBSession
from bddrest import When, Then, Given, response, And


from wolf.models import Cryptomodule, Token
from wolf.tests.helpers import BDDTestClass


class ListTokenTestCase(BDDTestClass):

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

        second_token = Token()
        second_token.name = 'second_token'
        second_token.phone = 989121234567
        second_token.expire_date = date.today() - timedelta(days=1)
        second_token.seed = b'\xdb!\x8e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz'
        second_token.is_active = True
        second_token.cryptomodule = mockup_cryptomodule
        DBSession.add(second_token)

        third_token = Token()
        third_token.name = 'third_token'
        third_token.phone = 989121234568
        third_token.expire_date = date.today() - timedelta(days=1)
        third_token.seed = b'\xdc!\x8e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz'
        third_token.is_active = True
        third_token.cryptomodule = mockup_cryptomodule
        DBSession.add(third_token)

        DBSession.commit()
        cls.mockup_cryptomodule_id = mockup_cryptomodule.id

    def test_list_token(self):
        call = self.call(
            title='Token list',
            description='List of tokens',
            url='/apiv1/tokens',
            verb='LIST',
        )

        with Given(call):
            Then(response.status_code == 200)
            And(len(response.json) == 3)

            When(
                'Trying to get list of tokens with phone query string',
                query=dict(
                    phone=989121234567
                )
            )
            Then(response.status_code == 200)
            And(len(response.json) == 2)
            And('id' in response.json[0])
            And('id' in response.json[1])
            And(response.json[0]['phone'] == 989121234567)
            And(response.json[1]['phone'] == 989121234567)

            When(
                'Trying to get list of tokens with take query string',
                query=dict(
                    take=2
                )
            )
            Then(response.status_code == 200)
            And(len(response.json) == 2)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
