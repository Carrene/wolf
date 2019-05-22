from datetime import datetime

from bddrest import when, response, status, given

from wolf.models import Token, Cryptomodule
from wolf.tests.helpers import TimeMonkeyPatch, LocalApplicationTestCase


class TestOtpGenerate(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()

        cryptomodule = Cryptomodule()
        cryptomodule.one_time_password_length = 7
        session.add(cryptomodule)

        cls.token1 = token1 = Token()
        token1.name = 'token1'
        token1.phone = 1
        token1.bank_id = 2
        token1.expire_date = datetime(2074, 2, 21)
        token1.seed = \
            b"d\xd6p\x84\xd8\xd8V'\xe9(\x15\xfa\x162\xdd\t\x8f\x02\xbb>"
        token1.is_active = True
        token1.cryptomodule = Cryptomodule()
        session.add(token1)

        cls.token2 = token2 = Token()
        token2.name = 'token2'
        token2.phone = 2
        token2.bank_id = 2
        token2.expire_date = datetime(2074, 2, 21)
        token2.seed = \
            b'K\xeds\xbb[@\xce+\xca$l\xf6\xd3\x82\x8b\x04\xf0\x0b\x08\x02'
        token2.is_active = True
        token2.cryptomodule = cryptomodule
        session.add(token2)

        cls.expired_token = expired_token = Token()
        expired_token.name = 'expired_token'
        expired_token.phone = 3
        expired_token.bank_id = 2
        expired_token.expire_date = datetime(1970, 3, 1)
        expired_token.seed = \
            b'K\xedb\xbb[@\xce+\xca$l\xf6\xd3\x82\x8b\x04\xf0\x0b\x08\x02'
        expired_token.is_active = True
        expired_token.cryptomodule = cryptomodule
        session.add(expired_token)

        cls.deactivated_token = deactivated_token = Token()
        deactivated_token.name = 'deactivated_token'
        deactivated_token.phone = 4
        deactivated_token.bank_id = 2
        deactivated_token.expire_date = datetime(2074, 2, 21)
        deactivated_token.seed = \
            b'K\xedc\xbb[@\xce+\xca$l\xf6\xd3\x82\x8b\x04\xf0\x0b\x08\x02'
        deactivated_token.is_active = False
        deactivated_token.cryptomodule = cryptomodule
        session.add(deactivated_token)

        session.commit()

        cls.otp_time = 10001000

    def test_otp_generate(self):
        self.login_as_switchcard()

        with TimeMonkeyPatch(self.otp_time), self.given(
                'Create time based OTP with cryptomodule 1',
                f'/apiv1/tokens/token_id: {self.token1.id}/codes',
                'GENERATE',
        ):
            assert status == 200
            assert response.json['code'] == '3364'

            when(
                'Create time based OTP with cryptomodule 2',
                url_parameters=given | dict(token_id=self.token2.id)
            )
            assert status == 200
            assert response.json['code'] == '6816565'

            when(
                'Token is expired',
                url_parameters=given | dict(token_id=self.expired_token.id)
            )
            assert status == '602 Token is expired'

            when(
                'Token is deactivated',
                url_parameters=given | dict(token_id=self.deactivated_token.id)
            )
            assert status == '603 Token is deactivated'

            when(
                'Try to generate code with wrong token id',
                url_parameters=given | dict(token_id=5)
            )
            assert status == 404

            when(
                'Try to send form',
                form=dict(a='a')
            )
            assert status == '400 Form Not Allowed'

