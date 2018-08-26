import binascii
import hashlib
import time

import redis
from nanohttp import json, context, action, settings, RestController, \
    HTTPBadRequest, HTTPStatus, HTTPNotFound, LazyAttribute, Controller, \
    validate
from oathcy.otp import TOTP
from restfulpy.controllers import ModelRestController, RootController
from restfulpy.orm import commit, DBSession
from sqlalchemy import text, extract, event

import wolf
from wolf import cryptoutil
from wolf.exceptions import DeviceNotFoundError, DeactivatedTokenError, \
    ExpiredTokenError
from wolf.models import Device, Cryptomodule, Token


cached_cryptomodules = None


# FIXME: Move it to models.pyx
class MiniToken:
    _redis = None

    def __init__(self, id, seed, expire_date, is_active, cryptomodule_id, last_code=None,
                 same_code_verify_counter=0):
        self.id = id
        self.seed = seed
        self.expire_date = expire_date
        self.is_active = is_active
        self.cryptomodule_id = cryptomodule_id
        self.last_code = last_code
        self.same_code_verify_counter = same_code_verify_counter

    @staticmethod
    def create_blocking_redis_client():
        return redis.StrictRedis(
            host=settings.token.redis.host,
            port=settings.token.redis.port,
            db=settings.token.redis.db,
            password=settings.token.redis.password,
            max_connections=settings.token.redis.max_connections,
            socket_timeout=settings.token.redis.socket_timeout
        )

    @classmethod
    def redis(cls):
        if cls._redis is None:
            cls._redis = cls.create_blocking_redis_client()
        return cls._redis

    @classmethod
    def load_from_database(cls, token_id):
        row = DBSession.query(
            Token.id,
            Token.seed,
            extract('epoch', Token.expire_date),
            Token.activated_at.isnot(None),
            Token.cryptomodule_id,
        ).filter(Token.id == token_id).one_or_none()
        return cls(*row) if row else None

    @classmethod
    def load(cls, token_id, cache=False):
        if cache:
            token = cls.load_from_cache(token_id)
            if token is not None:
                return token
        return cls.load_from_database(token_id)

    @property
    def is_expired(self):
        return self.expire_date <= time.time()

    @property
    def cryptomodules(self):
        global cached_cryptomodules
        if cached_cryptomodules is None:
            modules = {}
            for m in DBSession.execute(text(
                'SELECT id, time_interval, one_time_password_length FROM cryptomodule'
                )):
                modules[m[0]] = m
            cached_cryptomodules = modules
        return cached_cryptomodules

    @property
    def cryptomodule(self):
        return self.cryptomodules[self.cryptomodule_id]

    @property
    def time_interval(self):
        return self.cryptomodule[1]

    @property
    def length(self):
        return self.cryptomodule[2]

    def verify(self, code, window):
        if self.last_code == code:
            self.same_code_verify_counter += 1
            if settings.token.verify_limit < self.same_code_verify_counter:
                return False
        else:
            self.last_code = code
            self.same_code_verify_counter = 0

        pinblock = cryptoutil.EncryptedISOPinBlock(self.id)
        otp = pinblock.decode(code)
        return \
            TOTP(self.seed, time.time(), self.length, step=self.time_interval)\
            .verify(otp, window)

    def cache(self):
        self.redis().set(
            str(self.id),
            b'%s,%d,%d,%d,%s,%d' % (
                binascii.hexlify(self.seed),
                int(self.expire_date),
                int(self.is_active),
                self.cryptomodule_id,
                self.last_code,
                self.same_code_verify_counter
            )
        )

    @classmethod
    def load_from_cache(cls, token_id):
        cache_key = str(token_id)
        redis = cls.redis()
        if redis.exists(cache_key):
            token = redis.get(cache_key).split(b',')
            return cls(
                token_id,
                binascii.unhexlify(token[0]),
                float(token[1]),
                bool(token[2]),
                int(token[3]),
                token[4],
                int(token[5])
            ) if token else None
        return None

    @classmethod
    def invalidate(cls, token_id):
        cls.redis().delete(token_id)

    @classmethod
    def after_update(cls, mapper, connection, target):
        if settings.token.redis.enabled:
            cls.invalidate(target.id)

event.listen(Token, 'after_update', MiniToken.after_update)


class CodesController(RestController):

    @LazyAttribute
    def window(self):
        return settings.oath.window

    @action
    def verify(self, token_id, code):
        print(f'Verifying token_id={token_id} code={code}')
        token = MiniToken.load(token_id, cache=settings.token.redis.enabled)
        if token is None:
            raise HTTPNotFound()

        if token.is_expired:
            raise ExpiredTokenError()

        if not token.is_active:
            raise DeactivatedTokenError()

        try:
            is_valid = token.verify(
                code.encode(),
                self.window,
            )
            token.cache()
        except ValueError:
            is_valid = False

        if not is_valid:
            raise HTTPBadRequest('Invalid Code')


class TokenController(ModelRestController):
    __model__ = Token

    def __init__(self):
        super().__init__()
        self.codes_controller = CodesController()

    def __call__(self, *remaining_paths):
        if len(remaining_paths) > 1 and remaining_paths[1] == 'codes':
            return self.codes_controller(remaining_paths[0], *remaining_paths[2:])
        return super().__call__(*remaining_paths)

    @staticmethod
    def _validate_token(token):
        if token.is_expired:
            raise ExpiredTokenError()

        if not token.is_active:
            raise DeactivatedTokenError()

    @staticmethod
    def _ensure_device():
        phone = int(context.form['phone'])

        # Checking the device
        device = DBSession.query(Device) \
            .filter(Device.phone == phone) \
            .one_or_none()

        # Adding a device also
        if device is None:
            raise DeviceNotFoundError()
        return device

    @staticmethod
    def _find_or_create_token():
        name = context.form['name']
        phone = context.form['phone']
        cryptomodule_id = context.form['cryptomoduleId']

        if DBSession.query(Cryptomodule) \
                .filter(Cryptomodule.id == cryptomodule_id) \
                .count() <= 0:
            raise HTTPStatus('472 Invalid cryptomodule id')

        token = DBSession.query(Token).filter(
            Token.name == name,
            Token.cryptomodule_id == cryptomodule_id,
            Token.phone == phone
        ).one_or_none()

        if token is None:
            # Creating a new token
            token = Token()
            token.update_from_request()
            token.is_active = True
            token.initialize_seed()
            DBSession.add(token)
        DBSession.flush()
        return token

    @json
    @validate(
        name=dict(
            required='467 name required',
        ),
        phone=dict(
            required='468 phone required',
            type_=int
        ),
        cryptomoduleId=dict(
            required='469 cryptomoduleId required',
            type_=(int, '471 cryptomoduleId must be integer')
        ),
        expireDate=dict(
            required='470 expireDate required',
            type_=float
        )
    )
    @Token.expose
    @commit
    def ensure(self):
        # TODO: type validation
        device = self._ensure_device()
        token = self._find_or_create_token()
        self._validate_token(token)
        DBSession.flush()
        result = token.to_dict()
        result['provisioning'] = token.provision(device.secret)
        return result


challenge_pattern = r'^[a-zA-Z0-9]{5,25}$'


class DeviceController(ModelRestController):
    __model__ = Device

    @json
    # TODO: Use model validation
    @Device.expose
    @commit
    def register(self):
        phone = context.form['phone']
        udid = context.form['udid']
        device = DBSession.query(Device) \
            .filter(Device.phone == phone) \
            .one_or_none()

        if device is None:
            device = Device()
            DBSession.add(device)
            device.phone = phone

        secret_key = hashlib.pbkdf2_hmac(
            'sha256',
            str(phone).encode() + udid.encode(),
            cryptoutil.random(32),
            100000,
            dklen=32
        )
        device.secret = secret_key
        return device


class ApiV1(Controller):
    tokens = TokenController()
    devices = DeviceController()

    @json
    def version(self):
        return {
            'version': wolf.__version__
        }


class Root(RootController):
    apiv1 = ApiV1()

