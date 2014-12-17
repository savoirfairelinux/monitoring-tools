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

def _get_if_not_none(value):
    return value if value is not None else ''


class PerfData(object):
    """
    An object holding a plugin performance data, and whose string
    representation matches the one needed in a plugin output.
    """
    def __init__(self, label, value, unit=None, warn=None, crit=None, min_=None, max_=None):
        # if None is passed (coming e.g. from arg.get('warning'), makes sure
        # the empty string is used instead
        self.label = label
        self.value = value
        self.unit = _get_if_not_none(unit)
        self.warn = _get_if_not_none(warn)
        self.crit = _get_if_not_none(crit)
        self.min_ = _get_if_not_none(min_)
        self.max_ = _get_if_not_none(max_)
    
    def __repr__(self):
        return ('%(label)s=%(value)s%(unit)s;%(warn)s;%(crit)s;%(min_)s;%(max_)s'
                % self.__dict__)

#############################################################################
