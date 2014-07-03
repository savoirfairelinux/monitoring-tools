#!/usr/bin/python
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
#            webserver.py Create a webserver to run unit tests
#
#
#  Author: Thibault Cohen <thibault.cohen@savoirfairelinux.com> 
#
#

import sys
import os
import getopt
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

def run_webserver(args):
    HandlerClass = SimpleHTTPRequestHandler
    ServerClass  = BaseHTTPServer.HTTPServer
    Protocol     = "HTTP/1.0"

    os.chdir(args['document'])

    port = args['port']
    server_address = (args['hostname'], port)

    HandlerClass.protocol_version = Protocol
    httpd = ServerClass(server_address, HandlerClass)

    sa = httpd.socket.getsockname()
    httpd.serve_forever()


def main():
    """Main fonction
    """
    try:
        options, args = getopt.getopt(sys.argv[1:],
                        'H:p:d:',
                        ['hostname=', 'port=',
                         'document-root'])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(1)

    args = {}

    for option_name, value in options:
        if option_name in ("-H", "--hostname"):
            args['hostname'] = value
        elif option_name in ("-p", "--port"):
            args['port'] = value
        elif option_name in ("-d", "--document-root"):
            args['document'] = value

    if not 'hostname' in args:
        args['hostname'] = "127.0.0.1"
    if not 'port' in args:
        args['port'] = 51515
    else:
        args['port'] = int(args['port'])
    if not 'document' in args:
        args['document'] = "."

    run_webserver(args)


if __name__ == "__main__":
    main()

