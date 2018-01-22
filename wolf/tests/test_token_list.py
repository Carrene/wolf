import unittest
from datetime import date, timedelta

from nanohttp import settings
from restfulpy.orm import DBSession
from bddrest import when, then, given, response, and_


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
        first_token.consecutive_tries = 5
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
        call = dict(
            title='Token list',
            description='List of tokens',
            url='/apiv1/tokens',
            verb='LIST',
        )

        with self.given(**call):
            then(response.status_code == 200)
            and_(len(response.json) == 3)

            when(
                'Trying to get list of tokens sorted by id ascending',
                query=dict(
                    sort='id'
                )
            )
            then(response.status_code == 200)
            result = response.json
            and_(len(result) == 3)
            and_(result[0]['id'] == 1)
            and_(result[1]['id'] == 2)
            and_(result[2]['id'] == 3)
            and_(result[0]['isLocked'] is True)
            and_(result[1]['isLocked'] is False)
            and_(result[2]['isLocked'] is False)
            and_(result[0]['isExpired'] is False)
            and_(result[1]['isExpired'] is True)
            and_(result[2]['isExpired'] is True)

            when(
                'Trying to get list of tokens sorted by id descending',
                query=dict(
                    sort='-id'
                )
            )
            then(response.status_code == 200)
            result = response.json
            and_(len(result) == 3)
            and_(result[0]['id'] == 3)
            and_(result[1]['id'] == 2)
            and_(result[2]['id'] == 1)

            when(
                'Trying to get list of tokens with phone query string',
                query=dict(
                    phone=989121234567
                )
            )
            then(response.status_code == 200)
            and_(len(response.json) == 2)
            and_('id' in response.json[0])
            and_('id' in response.json[1])
            and_(response.json[0]['phone'] == 989121234567)
            and_(response.json[1]['phone'] == 989121234567)

            when(
                'Trying to get list of tokens with take query string',
                query=dict(
                    take=2
                )
            )
            then(response.status_code == 200)
            and_(len(response.json) == 2)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
