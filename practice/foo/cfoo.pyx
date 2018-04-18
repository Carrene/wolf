from nanohttp import configure, Controller, quickstart, text


class Root(Controller):
    @text
    def index(self):
        return 'Hello'

