from nanohttp import Controller, json
from restfulpy.controllers import RootController

import wolf
from wolf.controllers.devices import DeviceController
from wolf.controllers.cryptomodules import CryptomoduleController
from wolf.controllers.tokens import TokenController


class ApiV1(Controller):
    cryptomodules = CryptomoduleController()
    tokens = TokenController()
    devices = DeviceController()

    @json
    def version(self):
        return {
            'version': wolf.__version__
        }


class Root(RootController):
    apiv1 = ApiV1()
