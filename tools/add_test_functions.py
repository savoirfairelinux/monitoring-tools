#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fileinput

tag = "if __name__ == '__main__':"

opts = ["file", "name", "options", "return_code", "regexp"]
prop = {}

for opt in opts:
    prop[opt] = raw_input("Please specify %s :\n" % opt)

test_fun = ("""    def %(name)s(self):
        \"\"\"Test %(name)s :
        %(options)s
        \"\"\"
        sys.argv = [sys.argv[0]]
""" % prop)

for opt in prop['options'].split(" "):
    test_fun += " " * 8 + "sys.argv.append('%s')\n" % opt

test_fun += " " * 8 + "self.do_tst(%(return_code)s, \"%(regexp)s\")\n" % prop

for line in fileinput.input(prop['file'], inplace=1):
    if line.startswith(tag):
        print test_fun
    print line,
