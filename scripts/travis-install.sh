#!/usr/bin/env bash

# Use this to encrypt files
# $ tar -f travis-keys.tar travis-wolf_rsa travis-oath.cy_rsa
# $ travis encrypt-file travis-keys.tar
# $ rm travis-keys.tar

ENCRYPTED_KEY_VAR="encrypted_${ENCRYPTION_LABEL}_key"
ENCRYPTED_IV_VAR="encrypted_${ENCRYPTION_LABEL}_iv"
ENCRYPTED_KEY=${!ENCRYPTED_KEY_VAR}
ENCRYPTED_IV=${!ENCRYPTED_IV_VAR}
OUT_FILE="travis-keys.tar"
openssl aes-256-cbc -K $ENCRYPTED_KEY -iv $ENCRYPTED_IV -in "${OUT_FILE}.enc" -out "$OUT_FILE" -d
tar -xf travis-keys.tar
chmod 600 travis-wolf_rsa
chmod 600 travis-oath.cy_rsa
eval `ssh-agent -s`
ssh-add travis-wolf_rsa
ssh-add travis-oath.cy_rsa

pip3 install -U pip setuptools wheel cython
pip3 install -U coverage coveralls
pip3 install --upgrade git+ssh://git@github.com/Carrene/oath.cy.git
pip3 install -e .

