import unittest

from restfulpy.testing.documentation import FormParameter

from wolf.tests.helpers import WebTestCase, As


# https://github.com/Carrene/wolf/wiki/User-Stories#generate-crypto-module
class GenerateOathCryptomoduleTestCase(WebTestCase):
    url = '/apiv1/cryptomodules'

    def test_generate_oath_cryptomodule(self):
        provider_reference = 1
        hash_algorithm = 'SHA-512'
        counter_type = 'time'
        time_interval = 120
        one_time_password_length = 4
        challenge_response_length = 6

        result, ___ = self.request(
            As.provider, 'GENERATE', self.url,
            params=[
                FormParameter('providerReference', provider_reference, type_=int),
                FormParameter('hashAlgorithm', hash_algorithm),
                FormParameter('counterType', counter_type),
                FormParameter('timeInterval', time_interval, type_=int),
                FormParameter('oneTimePasswordLength', one_time_password_length, type_=int),
                FormParameter('challengeResponseLength', challenge_response_length, type_=int),
            ]
        )

        self.assertDictContainsSubset(
            result,
            {
                'providerReference': provider_reference,
                'hashAlgorithm': hash_algorithm,
                'counterType': counter_type,
                'timeInterval': time_interval,
                'isActive': True,
                'oneTimePasswordLength': one_time_password_length,
                'challengeResponseLength': challenge_response_length,
            }
        )

        self.assertIn('id', result)
        self.assertIn('createdAt', result)
        self.assertIn('modifiedAt', result)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
