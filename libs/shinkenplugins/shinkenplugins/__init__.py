# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Copyright (C) 2014, Savoir-faire Linux, Inc.

# Authors:
#   Grégory Starck <gregory.starck@savoirfairelinux.com>
#   Matthieu Caneill <matthieu.caneill@savoirfairelinux.com>
#   Sébastien Coavoux <sebastien.coavoux@savoirfairelinux.com>
#
#############################################################################

# This is a namespace package so don't expect this __init__
# to be always executed. let alone be installed.

__import__('pkg_resources').declare_namespace(__name__)

# See for references:
# https://pythonhosted.org/setuptools/setuptools.html#namespace-packages
# http://stackoverflow.com/questions/27715334/with-setuptools-when-does-namespace-packages-init-py-files-disappears
# or
# http://stackoverflow.com/questions/24347094/python-setuptools-init-py-does-not-call-declare-namespace
