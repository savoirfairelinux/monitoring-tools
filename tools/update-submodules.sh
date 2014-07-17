#!/bin/bash

# Update submodules
git submodule update --init
git submodule foreach 'git checkout master && git pull origin master'
git add plugin-*

# Update documentation
rm doc/source/plugin-*.rst
cp plugins/*/doc/*.rst doc/source/
git add doc/source/*.rst

git commit
