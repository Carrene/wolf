#!/usr/bin/env bash

set -e # Exit with nonzero exit code if anything fails

# Save some useful information
REPO_URL=`git config remote.origin.url`
SHA=`git rev-parse --verify HEAD`

# Get the deploy key by using Travis's stored variables to decrypt deploy_key.enc
ENCRYPTED_KEY_VAR="encrypted_${ENCRYPTION_LABEL}_key"
ENCRYPTED_IV_VAR="encrypted_${ENCRYPTION_LABEL}_iv"
ENCRYPTED_KEY=${!ENCRYPTED_KEY_VAR}
ENCRYPTED_IV=${!ENCRYPTED_IV_VAR}
OUT_KEY="travis-github-wiki-rsa"
openssl aes-256-cbc -K $ENCRYPTED_KEY -iv $ENCRYPTED_IV -in "${OUT_KEY}.enc" -out "$OUT_KEY" -d
chmod 600 $OUT_KEY
eval `ssh-agent -s`
ssh-add $OUT_KEY


# Clone/checkout the wiki branch from Github alongside the master branch working copy directory :
rm -rf ../project-wiki
git -C .. clone git@github.com:Carrene/wolf.wiki.git project-wiki
GIT="git -C ../project-wiki"
$GIT pull origin master
$GIT rm \*.md
cp data/api-documents/api/*.md ../project-wiki/
$GIT add \*.md
$GIT config user.name "Travis CI"
$GIT config user.email "$COMMIT_AUTHOR_EMAIL"
$GIT commit -am "Deploy to GitHub WIKI: ${SHA}"
$GIT push origin master

