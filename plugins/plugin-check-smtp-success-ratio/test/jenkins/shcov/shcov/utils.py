######################################################################
##
## Copyright (C) 2008,  Simon Kagstrom
##
## Filename:      shcov_utils.py
## Author:        Simon Kagstrom <simon.kagstrom@gmail.com>
## Description:   Small utils :-)
##
## $Id:$
##
######################################################################
def read_file(name):
    f = open(name)
    out = f.read()
    f.close()
    return out
