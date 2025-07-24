#!/bin/bash

set -e

if [ -z "$1" ]
then
  echo 'Supply a version!'
  exit 1
fi

echo "Building Version ${1}"

cd "$(dirname "$0")/.."

rm -rf dist/*

echo "$1" > VERSION
python3 -m pip install -r ./requirements_build.txt >/dev/null
python3 -m build
# python3 -m twine upload --repository pypi dist/*
