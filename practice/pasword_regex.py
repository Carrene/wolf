#! /usr/bin/env python3.6
import re


whitelist = [
    'Foo1234!',
    'fooBAR!123456789',
]


blacklist = [
    # + is not allowed
    'Foo123!+',
    'Foo123!-',

    # Space is not allowed
    'Foo 123!',

    # At lease one capital character is required
    'foo1234!',

    # At lease one lowercase character is required
    'FOO1234!',

    # At lease one special character is required
    'Foo12345',

    # 8 <= length <= 16
    'Foo123!',
    'fooBAR1234567890!',
]


def isvalid(p):
    if len(p) < 8 or len(p) > 16:
        return False

    regex = re.compile('^(?=.*[-+ ]).*$')
    if regex.match(p):
        return False

    regex = re.compile('^(?=.*[a-z]).*$')
    if not regex.match(p):
        return False

    regex = re.compile('^(?=.*[A-Z]).*$')
    if not regex.match(p):
        return False

    regex = re.compile('^(?=.*[@#$%^&!)(]).*$')
    if not regex.match(p):
        return False

    regex = re.compile('^(?=.*[\d]).*$')
    if not regex.match(p):
        return False

    return True


print('########### Whitelist:')

for case in whitelist:
    if not isvalid(case):
        print(f'Failed: {case} is not matched')
    else:
        print(f'Matched: {case}')

print('########### Blacklists:')

for case in blacklist:
    if isvalid(case):
        print(f'Failed: {case} is matched!')
    else:
        print(f'Not Matched: {case}')
