import re
from os.path import join, dirname
from setuptools import setup, find_packages
from Cython.Build import cythonize

# reading package version (same way the sqlalchemy does)
with open(join(dirname(__file__), 'wolf', '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)

dependencies = [
    'restfulpy >= 0.47.0',
    'oathcy >= 1.2.4b1',
    'pycrypto',

    'bddrest >= 0.11.0b2',
    # deployment
    'gunicorn',
]


wolf_modules = cythonize(
    'wolf/**/*.pyx',
    compiler_directives={'linetrace': True}
)


setup(
    name="wolf",
    version=package_version,
    author="Netalic",
    author_email="mt@netalic.de",
    install_requires=dependencies,
    packages=find_packages('.', exclude=['*.tests']),
    include_package_data=True,
    ext_modules=wolf_modules,
    test_suite="wolf.tests",
    entry_points={
        'console_scripts': [
            'wolf = wolf:wolf.cli_main',
        ]
    }
)

