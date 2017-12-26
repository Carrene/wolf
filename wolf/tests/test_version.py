import unittest

from wolf.tests.helpers import As, WebTestCase


class VersionTestCase(WebTestCase):
    url = '/apiv1/version'

    def test_version(self):
        result, ___ = self.request(As.everyone, 'GET', self.url)
        self.assertIn('version', result)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
