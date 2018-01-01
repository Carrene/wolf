import unittest

from wolf.tests.helpers import DocumentaryTestCase


class VersionTestCase(DocumentaryTestCase):

    def test_version(self):
        response = self.call('Obtaining the backend version', 'GET', '/apiv1/version')
        self.assertIn('version', response.json)

        response = self.call('routing', 'GET', '/tokens/1/codes/5434534')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
