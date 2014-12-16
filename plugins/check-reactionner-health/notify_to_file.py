#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import getopt
import sys


def main():
    """Main fonction
    """
    try:
        options, args = getopt.getopt(sys.argv[1:], 'f:', ['file'])
    except getopt.GetoptError:
        print "Usage : notify_to_file -f <filename>"
        sys.exit(3)

    args = {}

    for option_name, value in options:
        if option_name in ("-f", "--file"):
            args['file'] = value

    if 'file' not in args.keys():
        print "Usage : notify_to_file -f <filename>"
        sys.exit(3)

    if os.path.isfile(args['file']):
        open(args['file'], "w").close()
    else:
        os.utime(args['file'], None)


if __name__ == "__main__":
    main()