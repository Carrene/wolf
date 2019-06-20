from wolf.cryptoutil import create_signature


def test_create_siganture():
    message = \
        '<CUSTOMERCODE><111001209483>'          \
        '<REQUESTDATE><2019-06-18 13:00:00>'    \
        '<REQUESTNUMBER><123423241><SESSIONID>' \
        '<E219A82AA3F04E029FD19B741302C31E>'

    expected_signature = \
        b't/\x85\x88\t\x9b\xcd\x10z\xf7\xc3>:\x8e9\xda\xdbf\x9af\xc5'     \
        b'zb9\x82\xa2\xca\x13b\x86\xc7I*\x1dY\xb5(A\x895\xbdL\xecM=:'     \
        b'V14\x8f\xb5\xb0+\xc0\xe5b\x97\xe1\xea\xa5c\xbd\x06\x89@\x15'    \
        b'\xb6\xec\xedU\xc7\xa0X)\x80{\x12\x1b\x88b\xce~H\x86g\xf0\x8d'   \
        b'\x00\x97\x16c\xedav\xe5\x1a\xb1\x93\xf5\xfe\xa9\t\xcb\x0c\xeea' \
        b'\x87\xc29\xa7]Dr\x9d\xbc\xfaw\x0c/\xcf{\x82j2\xc8v\xdfd'

    signature = create_signature(
        'wolf/private-key/maskan.pem',
        message.encode(),
        'sha1'
    )

    assert signature == expected_signature

