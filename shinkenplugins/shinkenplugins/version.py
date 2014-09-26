
from __future__ import with_statement

from os.path import join, abspath, dirname


with open(join(dirname(abspath(__file__)), 'VERSION')) as fh:
    __version__ = fh.readline().strip()
