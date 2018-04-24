#!/usr/bin/env bash

# Use this to encrypt files
# $ tar -cf travis-keys.tar travis-oathcy_rsa* travis-wolf_rsa*
# $ travis encrypt-file travis-keys.tar
# $ mv travis-oathcy_rsa* travis-wolf_rsa* travis-keys.tar ~/Dropbox/carrene-private/github-keys


openssl aes-256-cbc -K $encrypted_5a97bbf310b0_key -iv $encrypted_5a97bbf310b0_iv \
		-in travis-keys.tar.enc -out travis-keys.tar -d
tar -xf travis-keys.tar
chmod 600 travis-oathcy_rsa
chmod 600 travis-wolf_rsa
eval `ssh-agent -s`
ssh-add travis-oathcy_rsa
ssh-add travis-wolf_rsa

pip3 install -U pip setuptools wheel cython
pip3 install -U coverage coveralls
pip3 install -U git+ssh://git@github.com/Carrene/oath.cy.git
pip3 install -e .

