from os.path import dirname

from bddrest import response, status
from nanohttp import settings

import wolf
from wolf.tests.helpers import LocalApplicationTestCase


class TestInfo(LocalApplicationTestCase):

    def test_info(self):
        with self.given(
                'Applicatino info',
                '/apiv1/info',
        ):
            assert status == 200
            assert 'version' in response.json
            assert 'title' in response.json
            assert response.json['version'] == wolf.__version__
            assert response.json['title'] == settings.process_name

