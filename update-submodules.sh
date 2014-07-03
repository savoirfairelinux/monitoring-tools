#!/bin/bash

# Update submodules
git submodule update --init
git submodule foreach 'git checkout master && git pull origin master'
git add plugin-*

# Update documentation
rm doc/source/plugin-*.rst
cp plugin-*/doc/*.rst doc/source/
cp doc/source/index_base.txt doc/source/index.rst
ls | grep plugin- | awk '{print "   "$$1}' >> doc/source/index.rst
git add doc/source/*.rst

git commit
