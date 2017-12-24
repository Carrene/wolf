import hashlib

from nanohttp import json, context
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
    @validate_form(exact=['phone', 'clientFactor', 'deviceFactor'], types={'phone': int})
    @Device.expose
    @commit
    def register(self):
        phone = context.form['phone']
        device = Device.query.filter(Device.phone == phone).one_or_none()

        if device is None:
            device = Device()
            DBSession.add(device)
            device.phone = phone

        secret_key = hashlib.pbkdf2_hmac(
            'sha256',
            context.form['clientFactor'].encode() + context.form['deviceFactor'].encode(),
            cryptoutil.random(32),
            100000,
            dklen=32
        )
        device.secret = secret_key
        return device
