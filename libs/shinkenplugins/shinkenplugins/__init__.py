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

from __future__ import unicode_literals, print_function, absolute_import

#############################################################################
#############################################################################

from .old import STATES, BasePlugin
from .perfdata import PerfData
from .test import TestPlugin

#############################################################################

__import__('pkg_resources').declare_namespace(__name__)
