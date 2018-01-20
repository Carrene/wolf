import os
import uuid
from _sha256 import sha256

from restfulpy.orm import ModifiedMixin, DeclarativeBase, Field
from restfulpy.principal import JwtPrincipal, JwtRefreshToken
from sqlalchemy import Integer, Unicode
from sqlalchemy.orm import synonym


class Member(ModifiedMixin, DeclarativeBase):
    __tablename__ = 'member'

    id = Field(Integer, primary_key=True)
    username = Field(Unicode(64), index=True, min_length=4, label='Username', unique=True)

    _password = Field(
        'password', Unicode(128), index=True, json='password', protected=True, min_length=4, label='Password'
    )

    type = Field(Unicode(50))

    __mapper_args__ = {
        'polymorphic_identity': __tablename__,
        'polymorphic_on': type
    }

    @classmethod
    def _hash_password(cls, password):
        salt = sha256()
        salt.update(os.urandom(60))
        salt = salt.hexdigest()

        hashed_pass = sha256()
        # Make sure password is a str because we cannot hash unicode objects
        hashed_pass.update((password + salt).encode('utf-8'))
        hashed_pass = hashed_pass.hexdigest()

        password = salt + hashed_pass
        return password

    def _set_password(self, password):
        """Hash ``password`` on the fly and store its hashed version."""
        self._password = self._hash_password(password)

    def _get_password(self):
        """Return the hashed version of the password."""
        return self._password

    password = synonym('_password', descriptor=property(_get_password, _set_password), info=dict(protected=True))

    def validate_password(self, password):
        """
        Check the password against existing credentials.
        :param password: the password that was provided by the user to
            try and authenticate. This is the clear text version that we will
            need to match against the hashed one in the database.
        :type password: unicode object.
        :return: Whether the password is valid.
        :rtype: bool
        """
        hashed_pass = sha256()
        hashed_pass.update((password + self.password[:64]).encode('utf-8'))
        return self.password[64:] == hashed_pass.hexdigest()

    def create_jwt_principal(self, session_id=None):

        if session_id is None:
            session_id = str(uuid.uuid4())

        return JwtPrincipal(dict(
            id=self.id,
            username=self.username,
            roles=self.roles,
            sessionId=session_id
        ))

    def create_refresh_principal(self):
        return JwtRefreshToken(dict(
            id=self.id
        ))


class Admin(Member):
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    @property
    def roles(self):
        return ['admin']
