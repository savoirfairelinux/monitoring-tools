#!/bin/bash
git submodule foreach 'git checkout master && git pull origin master'
git add plugin-*
git commit
