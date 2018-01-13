from restfulpy.orm import DBSession

from wolf.models import Cryptomodule, Admin


def insert():
    mockup_cryptomodule1 = Cryptomodule()
    mockup_cryptomodule1.challenge_response_length = 4
    mockup_cryptomodule1.one_time_password_length = 4

    mockup_cryptomodule2 = Cryptomodule()
    mockup_cryptomodule2.challenge_response_length = 5
    mockup_cryptomodule2.one_time_password_length = 5

    DBSession.add(mockup_cryptomodule1)
    DBSession.add(mockup_cryptomodule2)

    admin = Admin()
    admin.username = 'admin'
    admin.password = '123456'

    DBSession.add(admin)

    DBSession.commit()
