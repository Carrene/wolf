#!/usr/bin/env bash


ENCRYPTED_KEY_VAR="encrypted_${ENCRYPTION_LABEL}_key"
ENCRYPTED_IV_VAR="encrypted_${ENCRYPTION_LABEL}_iv"
ENCRYPTED_KEY=${!ENCRYPTED_KEY_VAR}
ENCRYPTED_IV=${!ENCRYPTED_IV_VAR}
OUT_KEY="travis-github-oath.py-rsa"
openssl aes-256-cbc -K $ENCRYPTED_KEY -iv $ENCRYPTED_IV -in "${OUT_KEY}.enc" -out "$OUT_KEY" -d
chmod 600 $OUT_KEY
eval `ssh-agent -s`
ssh-add $OUT_KEY

pip3 install -U pip setuptools wheel cython
pip3 install -U coverage coveralls
pip3 install --upgrade git+ssh://git@github.com/Carrene/python-oath.git
pip3 install --upgrade git+ssh://git@github.com/Carrene/oath.py.git
pip3 install -e .
