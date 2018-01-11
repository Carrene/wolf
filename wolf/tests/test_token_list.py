import unittest
from datetime import date, timedelta

from nanohttp import settings
from restfulpy.orm import DBSession

from wolf.models import Cryptomodule, Token
from wolf.tests.helpers import DocumentaryTestCase


class ListTokenTestCase(DocumentaryTestCase):

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
        # Token list
        response = self.call_as_bank(
            'List of tokens',
            'LIST',
            '/apiv1/tokens'
        )
        self.assertEqual(len(response.json), 3)

        # Token list with a phone query
        response = self.call_as_bank(
            'List of tokens',
            'LIST',
            '/apiv1/tokens',
            query=dict(
                phone=989121234567,
                take=2
                )
        )

        self.assertEqual(len(response.json), 2)
        self.assertIsNotNone(response.json[0]['id'])
        self.assertIsNotNone(response.json[1]['id'])
        self.assertEqual(response.json[0]['phone'], 989121234567)
        self.assertEqual(response.json[1]['phone'], 989121234567)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
