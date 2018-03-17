from nanohttp import configure, quickstart

from cfoo import Root


if __name__ == '__main__':
    configure()
    quickstart(Root())
