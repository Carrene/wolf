import unittest

from restfulpy.orm import DBSession
from bddrest.authoring import when, then, given, response, and_

from wolf.models import Cryptomodule, Token
from wolf.tests.helpers import BDDTestClass


class DeleteTokenTestCase(BDDTestClass):

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
        call = dict(
            title='Delete a token',
            description='Delete a token by id',
            url=f'/apiv1/tokens/token_id: {self.mockup_first_token_id}',
            verb='DELETE',
        )

        with self.given(**call):
            then(response.status_code == 200)
            and_(response.json['id'] == self.mockup_first_token_id)

            when(
                'Trying to delete a none existence token',
                url_parameters=dict(token_id=0),
            )
            then(response.status_code == 404)

            when(
                'Trying to get a deleted token',
                url_parameters=dict(token_id=self.mockup_first_token_id),
                verb='GET',
            )
            then(response.status_code == 404)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
