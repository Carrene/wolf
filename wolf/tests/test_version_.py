import unittest

from wolf.tests.helpers import DocumentaryTestCase


class VersionTestCase(DocumentaryTestCase):

    def test_version(self):
        response = dict('Obtaining the backend version', 'GET', '/apiv1/version')
        self.assertIn('version', response.json)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
