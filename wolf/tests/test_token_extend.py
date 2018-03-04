import unittest

from nanohttp import settings
from restfulpy.orm import DBSession
from bddrest.authoring import when, then, given, response, and_

from wolf.models import Cryptomodule, Token
from wolf.tests.helpers import BDDTestClass


class ExtendTokenTestCase(BDDTestClass):

    @classmethod
    def mockup(cls):
        mockup_cryptomodule = Cryptomodule()
        DBSession.add(mockup_cryptomodule)

        expired_token = Token()
        expired_token.name = 'expired_token'
        expired_token.phone = 989121234567
        expired_token.expire_date = '2000-12-07T18:14:39.558891'
        expired_token.seed = b'\xda!\x8e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz'
        expired_token.is_active = True
        expired_token.consecutive_tries = settings.token.max_consecutive_tries + 1
        expired_token.cryptomodule = mockup_cryptomodule
        DBSession.add(expired_token)

        available_token = Token()
        available_token.name = 'available_token'
        available_token.phone = 989121234567
        available_token.expire_date = '2099-12-07T18:14:39.558891'
        available_token.seed = b'\xca!\x8e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz'
        available_token.is_active = True
        available_token.consecutive_tries = settings.token.max_consecutive_tries + 1
        available_token.cryptomodule = mockup_cryptomodule
        DBSession.add(available_token)

        DBSession.commit()
        cls.mockup_expired_token_id = expired_token.id
        cls.mockup_available_token_id = available_token.id
        cls.mockup_cryptomodule_id = mockup_cryptomodule.id

    def test_extend_token(self):
        call = dict(
            title='Extend a token',
            description='Extend a token by id',
            url=f'/apiv1/tokens/token_id: {self.mockup_expired_token_id}',
            verb='EXTEND',
            form={'expireDate': 1613434403},
        )

        with self.given(**call):
            then(response.status_code == 200)
            and_(response.json['id'] == self.mockup_expired_token_id)
            and_(response.json['expireDate'] == '2021-02-16')

            when(
                'Trying extend a none existence token',
                url_parameters=dict(token_id=0),
                form={'expireDate': 1613434403},
            )
            then(response.status_code == 404)

            when(
                'Trying to extend a expired token to a time that passed',
                url_parameters=dict(token_id=self.mockup_expired_token_id),
                form={'expireDate': 1513434403},
            )
            then(response.status_code == 400)
            and_(self.assertDictEqual(response.json, dict(
                message='Bad Request',
                description='expireDate must be grater that current expireDate.'
            )))

            when(
                'Trying to extend a not expired token to a time that is less than its expire date',
                url_parameters=dict(token_id=self.mockup_available_token_id),
                form={'expireDate': 1813434403},
            )
            then(response.status_code == 400)

            when(
                'Trying to extend a token with a un supported expireDate format',
                url_parameters=dict(token_id=self.mockup_expired_token_id),
                form={'expireDate': '2019-12-07T18:14:39.558891'},
            )
            then(response.status_code == 400)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
