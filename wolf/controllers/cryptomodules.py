import functools

from nanohttp import json
from nanohttp.exceptions import HttpNotFound
from restfulpy.controllers import ModelRestController
from restfulpy.orm import commit, DBSession
from restfulpy.validation import validate_form, prevent_form

from wolf.models.cryptomodule import OathCryptomodule


oath_validate_submit = functools.partial(
    validate_form,
    types={
        'providerReference': int,
        'hashAlgorithm': str,
        'counterType': str,
        'timeInterval': int,
        'oneTimePasswordLength': int,
        'challengeResponseLength': int
    },
    pattern={
        'hashAlgorithm': r'^SHA-(1|256|384|512)$',
        'counterType': r'^(time|counter)$'
    }
)


class CryptomoduleController(ModelRestController):
    __model__ = OathCryptomodule

    @json
    @prevent_form
    @__model__.expose
    def get(self, oath_cryptomodule_id: int):
        oath_cryptomodule = OathCryptomodule.query.filter(OathCryptomodule.id == oath_cryptomodule_id).one_or_none()
        if not oath_cryptomodule:
            raise HttpNotFound()
        return oath_cryptomodule

    @json
    @oath_validate_submit(exact=[
        'providerReference', 'hashAlgorithm', 'counterType', 'timeInterval', 'oneTimePasswordLength', 'challengeResponseLength'
    ])
    @__model__.expose
    @commit
    def generate(self):
        oath_cryptomodule = OathCryptomodule()
        oath_cryptomodule.update_from_request()
        oath_cryptomodule.is_active = True
        DBSession.add(oath_cryptomodule)
        return oath_cryptomodule

    @json
    @oath_validate_submit(whitelist=[
        'hashAlgorithm', 'counterType', 'timeInterval', 'oneTimePasswordLength', 'challengeResponseLength'
    ])
    @__model__.expose
    @commit
    def edit(self, oath_cryptomodule_id: int):
        oath_cryptomodule = OathCryptomodule.query.filter(OathCryptomodule.id == oath_cryptomodule_id).one_or_none()
        if not oath_cryptomodule:
            raise HttpNotFound()
        oath_cryptomodule.update_from_request()
        DBSession.add(oath_cryptomodule)
        return oath_cryptomodule

    @json
    @prevent_form
    @__model__.expose
    @commit
    def activate(self, oath_cryptomodule_id: int):
        oath_cryptomodule = OathCryptomodule.query.filter(OathCryptomodule.id == oath_cryptomodule_id).one_or_none()
        if not oath_cryptomodule:
            raise HttpNotFound()
        oath_cryptomodule.is_active = True
        return oath_cryptomodule

    @json
    @prevent_form
    @__model__.expose
    @commit
    def deactivate(self, oath_cryptomodule_id: int):
        oath_cryptomodule = OathCryptomodule.query.filter(OathCryptomodule.id == oath_cryptomodule_id).one_or_none()
        if not oath_cryptomodule:
            raise HttpNotFound()
        oath_cryptomodule.is_active = False
        return oath_cryptomodule

    @json
    @prevent_form
    @__model__.expose
    @commit
    def remove(self, oath_cryptomodule_id: int):
        oath_cryptomodule = OathCryptomodule.query.filter(OathCryptomodule.id == oath_cryptomodule_id).one_or_none()
        if not oath_cryptomodule:
            raise HttpNotFound()
        DBSession.delete(oath_cryptomodule)
        return oath_cryptomodule

