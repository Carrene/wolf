import hashlib

from nanohttp import json
from nanohttp.contexts import context
from nanohttp.exceptions import HttpConflict
from restfulpy.controllers import ModelRestController
from restfulpy.orm import commit, DBSession
from restfulpy.validation import validate_form

from wolf import cryptoutil
from wolf.models import Device

challenge_pattern = r'^[a-zA-Z0-9]{5,25}$'


class DeviceController(ModelRestController):
    __model__ = Device

    # FIXME Rename it to register
    @json
    @validate_form(exact=['referenceId', 'clientFactor', 'deviceFactor'], types={'referenceId': int})
    @Device.expose
    @commit
    def add(self):

        reference_id = context.form['referenceId']

        if Device.query.filter(Device.reference_id == reference_id).one_or_none():
            raise HttpConflict('This referenceId is already exists.', 'repetitious-ref-id')

        secret_key = hashlib.pbkdf2_hmac(
            'sha256',
            context.form['clientFactor'].encode() + context.form['deviceFactor'].encode(),
            cryptoutil.random(32),
            100000,
            dklen=32
        )

        device = Device()
        device.secret = secret_key
        device.reference_id = reference_id

        DBSession.add(device)
        return device
