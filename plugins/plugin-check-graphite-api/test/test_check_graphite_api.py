#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#  Copyright (C) 2012 Savoir-Faire Linux Inc.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#  Projects :
#            Shinken plugins
#
#  File :
#            test_check_graphite_api
#
#
#  Author: Sebastien Coavoux sebastien.coavoux@savoirfairelinux.com
#
#

import unittest
import sys
import subprocess
import re
import time
from StringIO import StringIO
import socket
import threading

sys.path.append("..")

import check_graphite_api

class NetEcho(threading.Thread):
    """ This class aims to replace 'nc -e' or 'nc -c' calls in some tests """

    def __init__(self, host='localhost', port=50000, echo='DEFAULT'):
        threading.Thread.__init__(self)
        self.port = port
        self.host = host
        self.echo = echo
        self.server_socket = self._create_server_socket()

    def _create_server_socket(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
        except Exception as e:
            print 'Bind failed: could not acquire port', self.port
            print e
            sys.exit(0)
        s.listen(5)

        return s

    def run(self):
        client, address = self.server_socket.accept()
        rec = client.recv(1024)
        client.send(self.echo)
        client.close()
        self.server_socket.close()

class TestPlugin(unittest.TestCase):

    def setUp(self):
        pass

    def test_help(self):
        """Test help output :
           -h
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-h')
        self.do_tst(3, """^check_graphite_api""")

    def test_version(self):
        """Test version output :
           -V
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-V')
        self.do_tst(3, "^check_graphite_api.py v%s" % check_graphite_api.PLUGIN_VERSION)

    def do_tst(self, return_val, pattern_to_search):
        try:
            out = StringIO()
            prev_out = sys.stdout
            sys.stdout = out
            check_graphite_api.main()
        except SystemExit, e:
            output = out.getvalue().strip()
            sys.stdout = prev_out
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, return_val)
            matches = re.search(pattern_to_search, output)
            assert matches is not None

    def test_default_args(self):
        """Test default_args :
        -v -u http://localhost:8080/graphite
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-u')
        sys.argv.append('http://localhost:8080/graphite')
        self.do_tst(3, "^UNKNOWN : Argument 'target' is missing !")

    def test_no_server(self):
        """Test test_no_server :
        -u http://localhost:8080/graphite -t hst.svc.graph
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('-u')
        sys.argv.append('http://localhost:8080/graphite')
        sys.argv.append('-t')
        sys.argv.append('hst.svc.graph')
        self.do_tst(3, "UNKNOWN : Cannot connect to url")

    def test_bad_opt(self):
        """Test test_bad_opt :
        --k
        """
        sys.argv = [sys.argv[0]]
        sys.argv.append('--k')
        self.do_tst(3, "^option --k not recognized")

class TestPluginWithSocket(unittest.TestCase):

    def setUp(self):
        self.nc = NetEcho(host='localhost', port=8080)
        self.nc.start()

    def tearDown(self):
        self.nc.join()

    def do_tst(self, return_val, pattern_to_search):
        try:
            out = StringIO()
            prev_out = sys.stdout
            sys.stdout = out
            check_graphite_api.main()
        except SystemExit, e:
            output = out.getvalue().strip()
            sys.stdout = prev_out
            print output
            print re.search(pattern_to_search, output)
            self.assertEquals(type(e), type(SystemExit()))
            self.assertEquals(e.code, return_val)
            matches = re.search(pattern_to_search, output)
            assert matches is not None

    def test_default_delay(self):
        """Test test_default_delay :
        -v -u http://localhost:8080/graphite -t hst.svc.graph
        """
        self.nc.echo = """[{"target": "hst.svc.graph", "datapoints": [[null, 1], [%s, 2]]}]""" % '22'
        sys.argv = [sys.argv[0]]
        sys.argv.append('-M')
        sys.argv.append('-u')
        sys.argv.append('http://localhost:8080/graphite')
        sys.argv.append('-t')
        sys.argv.append('hst.svc.graph')
        self.do_tst(0, "^OK : Data found$")

    def test_bad_json(self):
        """Test test_bad_json :
        -v -u http://localhost:8080/graphite -t hst.svc.graph
        """
        self.nc.echo = """[{"target": "hst.svc.graph", "datapoints": [[null, 1], [%s, 2]]}]""" % 'None'
        sys.argv = [sys.argv[0]]
        sys.argv.append('-u')
        sys.argv.append('http://localhost:8080/graphite')
        sys.argv.append('-t')
        sys.argv.append('hst.svc.graph')
        self.do_tst(3, "UNKNOWN : JSON not decoded$")

    def test_no_data(self):
        """Test test_no_data :
        -v -u http://localhost:8080/graphite -t hst.svc.graph
        """
        self.nc.echo = """[{"target": "hst.svc.graph", "datapoints": [[null, 1], [%s, 2]]}]""" % 'null'
        sys.argv = [sys.argv[0]]
        sys.argv.append('-u')
        sys.argv.append('http://localhost:8080/graphite')
        sys.argv.append('-t')
        sys.argv.append('hst.svc.graph')
        self.do_tst(2, "CRITICAL : No data found$")

if __name__ == '__main__':
    unittest.main()
