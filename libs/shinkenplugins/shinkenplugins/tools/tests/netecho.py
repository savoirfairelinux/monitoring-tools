#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' A very simple class aimed at answering a given answer on a given TCP port.
'''

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
#  Author: Grégory Starck <gregory.starck@savoirfairelinux.com>
#
#

import sys
import socket
import threading


class NetEcho(threading.Thread):
    """ This class aims to replace 'nc -e' or 'nc -c' calls in some tests """

    def __init__(self, host='localhost', port=0, echo='DEFAULT'):
        super(NetEcho, self).__init__()
        self.port = port
        self.host = host
        self.echo = echo
        self.server_socket = self._create_server_socket()
        self.running = True

    def _create_server_socket(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.settimeout(1)  # so to not block indefinitely in accept()..
            s.bind((self.host, self.port))
            if not self.port:
                self.port = s.getsockname()[1]
        except Exception as err:
            print('Could not prepare socket %s' % err)
            raise
        s.listen(5)
        return s

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            try:
                client, address = self.server_socket.accept()
            except socket.error:
                pass
            else:
                break
        else:
            return
        rec = client.recv(1024)
        client.send(self.echo)
        client.close()
        self.server_socket.close()
