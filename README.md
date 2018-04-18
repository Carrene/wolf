# Wolf

Mobile-Token 2.x tokenizer

[![Gitter](https://img.shields.io/gitter/room/Carrene/Mobile-Token.svg)](https://gitter.im/Carrene/Mobile-Token)

![alt text](https://static.carrene.com/images/wolf.jpg "Wolf")

branches
--------

### master

[![Build Status](https://travis-ci.com/Carrene/wolf.svg?token=eprq9y92Aqggf5smZccy&branch=master)](https://travis-ci.com/Carrene/wolf)
[![Coverage Status](https://coveralls.io/repos/github/Carrene/wolf/badge.svg?branch=master&t=FNpdQh)](https://coveralls.io/github/Carrene/wolf?branch=master)

### nightly

[![Build Status](https://travis-ci.com/Carrene/wolf.svg?token=eprq9y92Aqggf5smZccy&branch=nightly)](https://travis-ci.com/Carrene/wolf)
[![Coverage Status](https://coveralls.io/repos/github/Carrene/wolf/badge.svg?branch=nightly&t=FNpdQh)](https://coveralls.io/github/Carrene/wolf?branch=nightly)

### develop

[![Build Status](https://travis-ci.com/Carrene/wolf.svg?token=eprq9y92Aqggf5smZccy&branch=develop)](https://travis-ci.com/Carrene/wolf)
[![Coverage Status](https://coveralls.io/repos/github/Carrene/wolf/badge.svg?branch=develop&t=FNpdQh)](https://coveralls.io/github/Carrene/wolf?branch=develop)

Setting up development Environment on Linux
----------------------------------

### Installing Dependencies

    $ sudo apt-get install libass-dev libpq-dev postgresql \
        build-essential redis-server redis-tools

### Installing Python

We need **Python 3.6.1** or higher.
Install it using [this instruction](https://docs.python.org/3/using/index.html).

### Setup Python environment

    $ sudo pip3 install virtualenvwrapper
    $ echo "export VIRTUALENVWRAPPER_PYTHON=`which python3.6`" >> ~/.bashrc
    $ echo "alias v.activate=\"source $(which virtualenvwrapper.sh)\"" >> ~/.bashrc
    $ source ~/.bashrc
    $ v.activate
    $ mkvirtualenv --python=$(which python3.6) --no-site-packages wolf

#### Activating virtual environment
    
    $ workon wolf

#### Upgrade pip, setuptools and wheel to the latest version

    $ pip install -U pip setuptools wheel cython
  
### Installing Project (edit mode)

So, your changes will affect instantly on the installed version

#### wolf and oath.py
    
    $ cd /path/to/workspace
    $ git clone git@github.com:Carrene/wolf.git
    $ git clone git@github.com:Carrene/oath.py.git
    $ cd oath.py
    $ pip install -e .
    $ cd ../wolf
    $ pip install -e .

For running tests, you should install development requirements too:

    $ pip install -r requirements-dev.txt

#### Enabling the bash auto completion for wolf

    $ echo "eval \"\$(register-python-argcomplete wolf)\"" >> $VIRTUAL_ENV/bin/postactivate
    $ deactivate && workon wolf
    
### Setup Database

#### Configuration

Create a file named `~/.config/wolf.yml`

```yaml

db:
  url: postgresql://postgres:postgres@localhost/wolf_dev
  test_url: postgresql://postgres:postgres@localhost/wolf_test
  administrative_url: postgresql://postgres:postgres@localhost/postgres
   
   
```

#### Remove old abd create a new database **TAKE CARE ABOUT USING THAT**

    $ wolf admin create-db --drop --basedata --mockup

#### Drop old database: **TAKE CARE ABOUT USING THAT**

    $ wolf [-c path/to/config.yml] admin drop-db

#### Create database

    $ wolf [-c path/to/config.yml] admin create-db

Or, you can add `--drop` to drop the previously created database: **TAKE CARE ABOUT USING THAT**

    $ wolf [-c path/to/config.yml] admin create-db --drop
    
#### Create database object

    $ wolf [-c path/to/config.yml] admin setup-db

#### Database migration

    $ wolf migrate upgrade head

#### Insert Base data

    $ wolf [-c path/to/config.yml] admin base-data
    
#### Insert Mockup data

    $ wolf [-c path/to/config.yml] dev mockup-data
    
### Unittests

    $ nosetests
    
### Serving

- Using python builtin http server

```bash
$ wolf [-c path/to/config.yml] serve
```    

- Gunicorn

```bash
$ ./gunicorn
```
