from nanohttp import RestController, json, context, HttpBadRequest, HttpForbidden, HttpNotFound
from restfulpy.authorization import authorize
from restfulpy.logging_ import get_logger
from restfulpy.orm import DBSession, commit
from restfulpy.validation import validate_form


from wolf.models import Member

logger = get_logger('auth')


class MembersController(RestController):

    @staticmethod
    def ensure_member(id_):
        member = Member.query.filter(Member.id == id_).one_or_none()

        if member is None:
            raise HttpNotFound('Cannot find any member with id %s' % id_)

        return member

    @json
    def login(self):
        username = context.form.get('username')
        password = context.form.get('password')

        def bad():
            logger.info('Login failed: %s' % username)
            raise HttpBadRequest('Invalid username or password')

        if not (username and password):
            bad()

        logger.info('Trying to login: %s' % username)
        principal = context.application.__authenticator__.login((username, password))
        if principal is None:
            bad()

        return dict(token=principal.dump())

    @json
    @Member.expose
    @commit
    @authorize
    @validate_form(exact=['currentPassword', 'newPassword'])
    def change(self, member_id: int, inner_resource: str):
        if context.identity.id != int(member_id):
            raise HttpForbidden()

        if inner_resource != 'password':
            raise HttpNotFound()

        member = self.ensure_member(member_id)
        member.change_password(context.form.get('currentPassword'), context.form.get('newPassword'))
        DBSession.add(member)
        return {}
