import unittest

from bddrest import Then, Given, response, And

import wolf
from wolf.tests.helpers import BDDTestClass


class VersionTestCase(BDDTestClass):

    def test_version(self):
        call = self.call(
            title='Application version',
            description='Get application version',
            url='/apiv1/version',
            verb='GET',
        )

        with Given(call):
            Then(response.status_code == 200)
            And('version' in response.json)
            And(response.json['version'] == wolf.__version__)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
