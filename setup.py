import re
from os.path import join, dirname
from setuptools import setup, find_packages
from Cython.Build import cythonize

# reading package version (same way the sqlalchemy does)
with open(join(dirname(__file__), 'wolf', '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)

dependencies = [
    'restfulpy >= 0.37.1',
    'oathpy',
    'pycrypto',

    'bddrest',
    # deployment
    'gunicorn',
]

setup(
    name="wolf",
    version=package_version,
    author="Netalic",
    author_email="mt@netalic.de",
    install_requires=dependencies,
    packages=find_packages(),
    ext_modules=cythonize('wolf/**/*.pyx'),
    test_suite="wolf.tests",
    entry_points={
        'console_scripts': [
            'wolf = wolf:wolf.cli_main',
        ]
    }
)
