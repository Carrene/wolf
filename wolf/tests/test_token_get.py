import unittest

from nanohttp import settings
from restfulpy.orm import DBSession

from wolf.models import Cryptomodule, Token
from wolf.tests.helpers import DocumentaryTestCase


class GetTokenTestCase(DocumentaryTestCase):

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
        mockup_token_id = self.mockup_first_token_id
        none_existence_token_id = 0

        # Get a token
        response = self.call_as_bank(
            'Get a token',
            'GET',
            f'/apiv1/tokens/token_id: {mockup_token_id}'
        )
        self.assertEqual(response.json['id'], mockup_token_id)

        # Get a none existence token
        self.call_as_bank(
            'Get a none existence token',
            'GET',
            f'/apiv1/tokens/token_id: {none_existence_token_id}',
            status=404
        )

        # Get token without providing a token_id
        self.call_as_bank(
            'Get token without providing a token_id',
            'GET',
            f'/apiv1/tokens',
            status=404
        )


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
