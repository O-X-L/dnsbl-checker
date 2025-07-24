#!/bin/bash

set -e

if [ -z "$1" ]
then
  echo 'Supply a version!'
  exit 1
fi

VERSION="$1"
echo "Building Version ${VERSION}"

cd "$(dirname "$0")/.."

rm -rf dist/*

echo "$VERSION" > VERSION
python3 -m pip install -r ./requirements_build.txt >/dev/null
python3 -m build
if ls "dist/dnsbl-check-${VERSION}.tar.gz" >/dev/null
then
  mv "dist/dnsbl-check-${VERSION}.tar.gz" "dist/dnsbl_check-${VERSION}.tar.gz"
fi

# python3 -m twine upload --repository pypi dist/*
