import unittest

from bddrest import response, status

import wolf
from .helpers import LocalApplicationTestCase


class TestVersion(LocalApplicationTestCase):

    def test_version(self):
        with self.given(
            'Application version',
            '/apiv1/version',
        ):
            assert status == 200
            assert 'version' in response.json
            assert response.json['version'] == wolf.__version__

