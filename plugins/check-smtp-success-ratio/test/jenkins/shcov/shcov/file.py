######################################################################
##
## Copyright (C) 2008,  Simon Kagstrom
##
## Filename:      shcov_file.py
## Author:        Simon Kagstrom <simon.kagstrom@gmail.com>
## Description:   The shcov file class
##
## $Id:$
##
######################################################################
import pickle, os, fcntl, stat

try:
    import hashlib
    has_hashlib = True
except:
    import md5
    has_hashlib = False

from utils import *

def md5_new():
    if has_hashlib:
        return hashlib.md5()
    return md5.new()

class File:
    def __init__(self, path, source_path = None):
        self.path = path
        if source_path == None:
            self.source_path = path
        else:
            self.source_path = source_path
        self.basename = os.path.basename(path)
        self.lines = {}
        self.is_saved = False

        m = md5_new()
        m.update(read_file(self.source_path))

        st = os.lstat(self.source_path)
        self.source_file_ctime = st[stat.ST_CTIME]

        self.digest = m.digest()

    def get_source_ctime(self):
        """Return the creation time of the script"""
        return self.source_file_ctime

    def set_source_path(self, path):
        self.source_path = path

    def get_source_path(self):
        return self.source_path

    def has_been_saved(self):
        return self.is_saved

    def save(self, path):
        outfile = open(path, 'wb')

        pickle.dump(self, outfile)
        outfile.close()
        self.is_saved = True

    def merge_object(self, obj):
        """Merge another object into this """

        for k,v in obj.lines.items():
            # Add the line numbering from the other
            if self.lines.has_key(k):
                self.lines[k] = self.lines[k] + v
            else:
                self.lines[k] = v



    def merge_with_path(self, dst_path):
        """Merge another object at @a dst_path into this one"""

        # Create if not already there
        fd = os.open(dst_path, os.O_CREAT | os.O_RDWR)
        f = os.fdopen(fd, "r+")

        fcntl.lockf(fd, fcntl.LOCK_EX)
        try:
            src = pickle.load( f )
        except:
            # This is OK, might not exist
            src = File(self.path, self.source_path)
        f.seek(0)

        # If the digest matches, merge the other object into this one
        if src.digest == self.digest:
            self.merge_object(src)

        # And save it!
        pickle.dump(self, f)
        f.close() # Also unlocks the file

    def add_to_line(self, line_nr):
        line_nr = int(line_nr)
        try:
            self.lines[line_nr] = self.lines[line_nr] + 1
        except KeyError, e:
            self.lines[line_nr] = 1


def load(path, script_base = ''):
    file = pickle.load(open(path))
    source_file = read_file(script_base + file.path)

    m = md5_new()
    m.update(source_file)
    digest = m.digest()

    # File has changed
    if digest != file.digest:
        file = File(file.path, source_path = script_base + file.path)

    file.set_source_path(script_base + file.path)
    return file
