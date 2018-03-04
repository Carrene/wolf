import unittest

from nanohttp import settings
from restfulpy.orm import DBSession
from bddrest.authoring import when, then, given, response, and_

from wolf.models import Cryptomodule, Token
from wolf.tests.helpers import BDDTestClass


class UnlockTokenTestCase(BDDTestClass):

    @classmethod
    def mockup(cls):
        mockup_cryptomodule = Cryptomodule()
        DBSession.add(mockup_cryptomodule)

        unlock_token = Token()
        unlock_token.name = 'unlock_token'
        unlock_token.phone = 989121234567
        unlock_token.expire_date = '2000-12-07T18:14:39.558891'
        unlock_token.seed = b'\xda!\x8e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz'
        unlock_token.is_active = True
        unlock_token.consecutive_tries = 0
        unlock_token.cryptomodule = mockup_cryptomodule
        DBSession.add(unlock_token)

        locked_token = Token()
        locked_token.name = 'locked_token'
        locked_token.phone = 989121234567
        locked_token.expire_date = '2099-12-07T18:14:39.558891'
        locked_token.seed = b'\xca!\x8e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz'
        locked_token.is_active = True
        locked_token.consecutive_tries = settings.token.max_consecutive_tries + 1
        locked_token.cryptomodule = mockup_cryptomodule
        DBSession.add(locked_token)

        DBSession.commit()
        cls.mockup_unlock_token_id = unlock_token.id
        cls.mockup_locked_token_id = locked_token.id
        cls.mockup_cryptomodule_id = mockup_cryptomodule.id

    def test_unlock_token(self):
        call = dict(
            title='Unlock a token',
            description='Unlock a token by id',
            url=f'/apiv1/tokens/token_id: {self.mockup_locked_token_id}',
            verb='UNLOCK',
        )

        with self.given(**call):
            then(response.status_code == 200)
            and_(response.json['id'] == self.mockup_locked_token_id)

            when(
                'Trying to unlock a token that was unlocked before',
                url_parameters=dict(token_id=self.mockup_locked_token_id),
            )
            then(response.status_code == 466)

            when(
                'Trying to unlock a none existence token',
                url_parameters=dict(token_id=0),
            )
            then(response.status_code == 404)

            when(
                'Trying to Unlock an unlocked token',
                url_parameters=dict(token_id=self.mockup_unlock_token_id),
            )
            then(response.status_code == 466)
            and_(self.assertDictEqual(response.json, dict(
                message='Token is not locked',
                description='The max try limitation is not exceeded.'
            )))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
