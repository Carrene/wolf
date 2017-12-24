from restfulpy.orm import DBSession

from wolf.models import Device, Token, Cryptomodule


def insert_devices():
    mockup_device1 = Device()
    mockup_device1.reference_id = 1
    mockup_device1.secret = b'\xa1(\x05\xe1\x05\xb9\xc8c\xfb\x89\x87|\xf7"\xf0\xc4h\xe1$=\x81\xc8k\x17rD,p\x1a\xcfT!'

    mockup_device2 = Device()
    mockup_device2.reference_id = 2
    mockup_device2.secret = b'\xab\xcd4\x87XG\x89Wd\x95I\x028I\x894u4\xab\xc2444TTdVV\xb4\xc6Kn'

    mockup_device3 = Device()
    mockup_device3.reference_id = 3
    mockup_device3.secret = \
        b'\xef\xef\xef\xef\xefC\x87\x85\x83xEH\x93\x80\x94\xef\xac\xcc\xc0\x98\x90\x89\x028@9\x844\x95\x82\t4'

    DBSession.add(mockup_device1)
    DBSession.add(mockup_device2)
    DBSession.add(mockup_device3)


def insert_tokens():
    mockup_cryptomodule1 = Cryptomodule()
    mockup_cryptomodule1.one_time_password_length = 6

    mockup_cryptomodule2 = Cryptomodule()
    mockup_cryptomodule2.one_time_password_length = 6

    DBSession.add(mockup_cryptomodule1)
    DBSession.add(mockup_cryptomodule2)

    mockup_token1 = Token()
    mockup_token1.name = 'name1'
    mockup_token1.client_reference = 1
    mockup_token1.expire_date = '2059-12-07T18:14:39'
    mockup_token1.seed = \
        b'\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5' \
        b'\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xf5j\xaaz'
    mockup_token1.is_active = True
    mockup_token1.cryptomodule = mockup_cryptomodule1

    mockup_token2 = Token()
    mockup_token2.name = 'name2'
    mockup_token2.client_reference = 1
    mockup_token2.expire_date = '2049-12-07T18:14:39'
    mockup_token2.seed = \
        b'\xaa\xaa\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5' \
        b'\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz\xf5j\xac\xcc'

    mockup_token2.is_active = True
    mockup_token2.cryptomodule = mockup_cryptomodule1

    mockup_token3 = Token()
    mockup_token3.name = 'name3'
    mockup_token3.client_reference = 1
    mockup_token3.expire_date = '2029-12-07T18:14:39'
    mockup_token3.seed = \
        b'\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xad\xa2\x19\xebf\x1f\xf8\xa3\x9f\x98\xb0j\xb0\xb3_V\xaa' \
        b'\xa7\xf8h\xf5j\xaaz\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\x88\x88\x88\x88X\x88\x88\x88\x88\x88\x88\x88'
    mockup_token3.is_active = True
    mockup_token3.cryptomodule = mockup_cryptomodule2

    DBSession.add(mockup_token1)
    DBSession.add(mockup_token2)
    DBSession.add(mockup_token3)


def insert():
    insert_tokens()
    insert_devices()
    DBSession.commit()
