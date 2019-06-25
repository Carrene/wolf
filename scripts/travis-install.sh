#!/usr/bin/env bash

# Use this to encrypt files
# $ tar -cf travis-keys.tar travis-oathcy_rsa* travis-wiki_rsa*
# $ travis encrypt-file travis-keys.tar
# $ mv travis-*_rsa* travis-keys.tar ~/Dropbox/carrene-private/github-keys


openssl aes-256-cbc -K $encrypted_5a97bbf310b0_key -iv $encrypted_5a97bbf310b0_iv \
		-in travis-keys.tar.enc -out travis-keys.tar -d
tar -xf travis-keys.tar

chmod 600 travis-oathcy_rsa
chmod 600 travis-wiki_rsa

eval `ssh-agent -s`
ssh-add travis-oathcy_rsa
ssh-add travis-wiki_rsa

pip3 install -U pip setuptools wheel cython
pip3 install -U coverage coveralls pytest-cov
pip3 install -U git+ssh://git@github.com/Carrene/oath.cy.git
pip3 install -r requirements-ci.txt
pip3 install -e .

