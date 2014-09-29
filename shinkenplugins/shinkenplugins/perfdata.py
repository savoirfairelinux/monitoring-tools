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

class PerfData(object):
    """
    An object holding a plugin performance data, and whose string
    representation matches the one needed in a plugin output.
    """
    def __init__(self, label, value, unit='', warn='', crit='', min_='', max_=''):
        # if None is passed (coming e.g. from arg.get('warning'), makes sure
        # the empty string is used instead
        self.label = label
        self.value = value
        self.unit = unit or ''
        self.warn = warn or ''
        self.crit = crit or ''
        self.min_ = min_ or ''
        self.max_ = max_ or ''
    
    def __repr__(self):
        return ('%(label)s=%(value)s%(unit)s;%(warn)s;%(crit)s;%(min_)s;%(max_)s'
                % self.__dict__)

#############################################################################
