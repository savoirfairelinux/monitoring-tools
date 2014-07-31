#!/bin/bash
#
#
#     Copyright (C) 2012 Savoir-Faire Linux Inc.
#
#     This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program; if not, write to the Free Software
#     Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#     Projects :
#               SFL Shinken plugins
#
#     File :
#               prepare_environment.sh Prepare env for testing
#
#
#     Author: Sebastien Coavoux <sebastien.coavoux@savoirfairelinux.com> 
#
#

HASH=$(cat test/jenkins/requirements.tests.freeze requirements.freeze|md5sum|cut -d' ' -f1)
if [ -e last_env_hash ]; then
  OLDHASH=$(cat last_env_hash)
else
  OLDHASH=""
fi
echo $HASH > last_env_hash

echo OLD REQS HASH AND NEW REQS HASH: $OLDHASH $HASH


# Cache the environment if it hasn't changed.
if [ "$OLDHASH" != "$HASH" ]; then
  echo "ENVIRONMENT SPECS CHANGED - CREATING A NEW ENVIRONMENT"
  virtualenv --distribute --system-site-packages env
  . env/bin/activate
  pip install --upgrade pip
  pip install --upgrade -r requirements.freeze
  pip install --upgrade -r test/jenkins/requirements.tests.freeze
  rm -rf last_env
  cp -ar env last_env
else
  echo "ENVIRONMENT SPECS HAVE NOT CHANGED - USING CACHED ENVIRONMENT"
  cp -ar last_env env
  . env/bin/activate
fi;

pip install -e .
