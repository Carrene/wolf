import unittest

from oathpy import OCRASuite


class OcraSuiteTestCase(unittest.TestCase):
    def test_format(self):
        self.assertEqual(
            'OCRA-1:HOTP-SHA256-7:QA45-T2M',
            str(OCRASuite(
                counter_type='time',
                length=7,
                hash_algorithm='SHA-256',
                time_interval=120,
                challenge_limit=45
            ))
        )

        self.assertEqual(
            'OCRA-1:HOTP-SHA256-7:C-QA45',
            str(OCRASuite(
                counter_type='counter',
                length=7,
                hash_algorithm='SHA-256',
                challenge_limit=45
            ))
        )

        self.assertEqual(
            'OCRA-1:HOTP-SHA256-6:QA40-T40S',
            str(OCRASuite(
                counter_type='time',
                length=6,
                hash_algorithm='SHA-256',
                time_interval=40,
            ))
        )

        self.assertEqual(
            'OCRA-1:HOTP-SHA256-6:QA40-T7H',
            str(OCRASuite(
                counter_type='time',
                length=6,
                hash_algorithm='SHA-256',
                time_interval=60 * 60 * 7,
            ))
        )

        # Bad counter_type
        with self.assertRaises(ValueError):
            str(OCRASuite(
                counter_type='bad',
                length=7,
                hash_algorithm='SHA-256',
                time_interval=120,
                challenge_limit=45,
            ))

        # Bad length
        with self.assertRaises(ValueError):
            str(OCRASuite(
                counter_type='time',
                length=1,
                hash_algorithm='SHA-256',
                time_interval=120,
                challenge_limit=45,
            ))

        # Bad hash_algorithm
        with self.assertRaises(ValueError):
            str(OCRASuite(
                counter_type='time',
                length=7,
                hash_algorithm='bad',
                time_interval=120,
                challenge_limit=45,
            ))

        # Time without time_interval
        with self.assertRaises(ValueError):
            str(OCRASuite(
                counter_type='time',
                length=7,
                hash_algorithm='SHA-256',
                challenge_limit=45,
            ))

        # Bad challenge_limit
        with self.assertRaises(ValueError):
            str(OCRASuite(
                counter_type='time',
                length=7,
                hash_algorithm='SHA-256',
                time_interval=120,
                challenge_limit=1,
            ))

        # Bad time errors
        with self.assertRaises(ValueError):
            str(OCRASuite(
                counter_type='time',
                length=7,
                hash_algorithm='SHA-256',
                time_interval=0,
                challenge_limit=45,
            ))

        with self.assertRaises(ValueError):
            str(OCRASuite(
                counter_type='time',
                length=7,
                hash_algorithm='SHA-256',
                time_interval=60 * 5 + 1,
                challenge_limit=45,
            ))

        with self.assertRaises(ValueError):
            str(OCRASuite(
                counter_type='time',
                length=7,
                hash_algorithm='SHA-256',
                time_interval=60 * 60 * 5 + 1,
                challenge_limit=45,
            ))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
