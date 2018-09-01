#!/usr/bin/env bash

set -e # Exit with nonzero exit code if anything fails

TARGET="/var/log/www/html/wiki/wolf/$TRAVIS_BRANCH"
echo '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'
echo $TARGET
echo $TRAVIS_PULL_REQUEST
echo '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'

