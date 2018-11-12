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


Setting up development Environment on Linux
----------------------------------

### Installing Dependencies

    $ sudo apt-get install libpq-dev postgresql \
        build-essential redis-server redis-tools

### Installing Python

We need **Python 3.6.1** or higher.
Install it using [this instruction](https://docs.python.org/3/using/index.html).

  
### Installing Project (edit mode)

So, your changes will affect instantly on the installed version

#### wolf and oath.py


```bash
pip instal cython
git clone git@github.com:Carrene/oath.cy.git
cd oath.cy
pip install -e .
cd path/to/wolf
pip install -e .
```

For running tests, you should install development requirements too:

    $ pip install -r requirements-dev.txt


#### Configuration

Create a file named `~/.config/wolf.yml`

```yaml

db:
  url: postgresql://postgres:postgres@localhost/wolf_dev
  test_url: postgresql://postgres:postgres@localhost/wolf_test
  administrative_url: postgresql://postgres:postgres@localhost/postgres
   
   
```

#### Remove old abd create a new database **TAKE CARE ABOUT USING THAT**

    $ wolf db create --drop --basedata --mockup

#### Drop old database: **TAKE CARE ABOUT USING THAT**

    $ wolf [-c path/to/config.yml] db drop

#### Create database

    $ wolf [-c path/to/config.yml] db create

Or, you can add `--drop` to drop the previously created database: **TAKE CARE ABOUT USING THAT**

    $ wolf [-c path/to/config.yml] db create --drop
    
#### Create database object

    $ wolf [-c path/to/config.yml] db schema

#### Database migration

    $ wolf migrate upgrade head

#### Insert Base data

    $ wolf [-c path/to/config.yml] db basedata
    
#### Insert Mockup data

    $ wolf db mockup [count[prefix]]
    $ wolf [-c path/to/config.yml db mockup 200 01
    
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
