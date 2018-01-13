from nanohttp import Controller, json
from restfulpy.controllers import RootController

import wolf
from wolf.controllers.devices import DeviceController
from wolf.controllers.members import MembersController
from wolf.controllers.tokens import TokenController


class ApiV1(Controller):
    tokens = TokenController()
    devices = DeviceController()
    members = MembersController()

    @json
    def version(self):
        return {
            'version': wolf.__version__
        }


class Root(RootController):
    apiv1 = ApiV1()
