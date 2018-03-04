import unittest

from restfulpy.orm import DBSession

from wolf.models import Cryptomodule, Token
from wolf.tests.helpers import DocumentaryTestCase


class DeleteTokenTestCase(DocumentaryTestCase):

    @classmethod
    def mockup(cls):
        mockup_cryptomodule = Cryptomodule()
        DBSession.add(mockup_cryptomodule)

        first_token = Token()
        first_token.name = 'first_token'
        first_token.phone = 989121234567
        first_token.expire_date = '2000-12-07T18:14:39.558891'
        first_token.seed = b'\xda!\x8e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz'
        first_token.is_active = True
        first_token.consecutive_tries = 0
        first_token.cryptomodule = mockup_cryptomodule
        DBSession.add(first_token)

        DBSession.commit()
        cls.mockup_first_token_id = first_token.id
        cls.mockup_cryptomodule_id = mockup_cryptomodule.id

    def test_delete_token(self):
        first_mockup_token_id = self.mockup_first_token_id
        none_existence_token_id = 0

        # Delete a none existence token
        self.call_as_bank(
            'Delete a None existence token',
            'DELETE',
            f'/apiv1/tokens/token_id: {none_existence_token_id}',
            status=404
        )

        # Delete a token
        response = self.call_as_bank(
            'Delete a token',
            'DELETE',
            f'/apiv1/tokens/token_id: {first_mockup_token_id}',
        )

        self.assertEqual(response.json['id'], first_mockup_token_id)

        # Get a deleted token
        self.call_as_bank(
            'Get a deleted token',
            'Get',
            f'/apiv1/tokens/token_id: {first_mockup_token_id}',
            status=404
        )


if __name__ == '__main__':  # pragma: no cover
    unittest.main()