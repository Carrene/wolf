#!/usr/bin/env bash

set -e # Exit with nonzero exit code if anything fails

# Save some useful information
REPO_URL=`git config remote.origin.url`
SHA=`git rev-parse --verify HEAD`
if [ -z "$1" ]; then
  VERSION=`grep -P '^__version__ =' wolf/__init__.py | grep -oP \
    '([1-9]\d*!)?(0|[1-9]\d*)(\.(0|[1-9]\d*))*((a|b|rc)(0|[1-9]\d*))?(\.post(0|[1-9]\d*))?(\.dev(0|[1-9]\d*))?'`
  VERSION="v${VERSION}"
else
  VERSION=$1
fi
TARGET="../project-gh-pages/$VERSION"
# Clone/checkout the gh-pages branch from Github alongside the master branch working copy
# directory:
rm -rf ../project-gh-pages
git -C .. clone git@github.com:Carrene/wolf.git -b gh-pages project-gh-pages
GIT="git -C ../project-gh-pages"
$GIT rm --ignore-unmatch $VERSION/\*.md
mkdir -p $TARGET
cp data/documentation/*.md $TARGET
ls | egrep '^(v.*|nightly)' | perl -e 'print "<html><body><ul>"; while(<>) { chop $_; print "<li><a
 href=\"./$_\">$_</a></li>";} print "</ul></body></html>"' > ../project-gh-pages/index.html
$GIT add $VERSION/\*.md
$GIT add index.html
$GIT config user.name "Travis CI"
$GIT config user.email "$COMMIT_AUTHOR_EMAIL"
$GIT commit -am "Deploy to Github Pages: ${VERSION} ${SHA}"
$GIT push origin gh-pages

