import unittest

from nanohttp import settings
from restfulpy.orm import DBSession

from wolf.models import Cryptomodule, Token
from wolf.tests.helpers import DocumentaryTestCase


class ActivateTokenTestCase(DocumentaryTestCase):

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

        second_token = Token()
        second_token.name = 'second_token'
        second_token.phone = 989121234567
        second_token.expire_date = '2099-12-07T18:14:39.558891'
        second_token.seed = b'\xca!\x8e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz'
        second_token.is_active = False
        second_token.consecutive_tries = settings.token.max_consecutive_tries + 1
        second_token.cryptomodule = mockup_cryptomodule
        DBSession.add(second_token)

        DBSession.commit()
        cls.mockup_first_token_id = first_token.id
        cls.mockup_second_token_id = second_token.id
        cls.mockup_cryptomodule_id = mockup_cryptomodule.id

    def test_activate_token(self):
        first_mockup_token_id = self.mockup_first_token_id
        second_mockup_token_id = self.mockup_second_token_id
        none_existence_token_id = 0

        # Activate a none existence token
        self.call_as_bank(
            'Activate a None existence token',
            'ACTIVATE',
            f'/apiv1/tokens/token_id: {none_existence_token_id}',
            status=404
        )

        # Activate an active token
        response = self.call_as_bank(
            'Activate an active token',
            'ACTIVATE',
            f'/apiv1/tokens/token_id: {first_mockup_token_id}',
            status=409
        )

        self.assertDictEqual(
            response.json,
            {
                'message': 'Conflict',
                'description': 'Token is already active.'
            }
        )

        # Activate a token
        response = self.call_as_bank(
            'Activate a token',
            'ACTIVATE',
            f'/apiv1/tokens/token_id: {second_mockup_token_id}',
        )

        self.assertEqual(response.json['id'], second_mockup_token_id)
        self.assertTrue(response.json['isActive'])


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
