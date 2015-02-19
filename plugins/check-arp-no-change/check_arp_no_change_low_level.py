#!/usr/bin/env python
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

# Copyright (C) 2014, Grégory Starck <gregory.starck@savoirfairelinux.com>

#############################################################################

from shinkenplugins.old import BasePlugin
from shinkenplugins.states import STATES

DEFAULT_IFNAME = "eth0"

#############################################################################

import socket
from socket import AF_PACKET, SOCK_RAW
from struct import pack, unpack

import time


ARP_GRATUITOUS = 1
ARP_STANDARD = 2


def val2int(val):
    '''Retourne une valeur sous forme d'octet en valeur sous forme
       d'entier.'''

    return int(''.join(['%02d'%ord(c) for c in val]), 16)


# Classes :
###########

class ArpRequest:
    '''Génère une requête ARP et attend la réponse'''

    def __init__(self, ipaddr, if_name, arp_type=ARP_GRATUITOUS, timeout=3, arp_resend=0.4):
        # Initialisation du socket (socket brut, donc besoin d'ê root)
        self.arp_type = arp_type
        self.if_name = if_name
        self.ipaddr = ipaddr
        self.timeout = timeout
        self.arp_resend = arp_resend

    def request(self):
        '''Envois une requête arp et attend la réponse'''

        self.if_ipaddr = socket.gethostbyname(socket.gethostname())
        self.socket = socket.socket(AF_PACKET, SOCK_RAW, SOCK_RAW)
        try:
            self.socket.bind((self.if_name, SOCK_RAW))
            return self._make_request()
        finally:
            self.socket.close()

    def _make_request(self):
        # Envois de 3 requêtes ARP
        for _ in range(3):
            self._send_arp_request()

        time.sleep(0.05)

        # Puis attente de la réponse
        return self._wait_response()

    def _send_arp_request(self):
        '''Envois une requête ARP pour la machine'''

        # Adresse logicielle de l'émetteur :
        if self.arp_type == ARP_STANDARD:
            saddr = pack('!4B',
                           *[int(x) for x in self.if_ipaddr.split('.')])
        else:
            saddr = pack('!4B',
                              *[int(x) for x in self.ipaddr.split('.')])


        # Forge de la trame :
        frame = [
            ### Partie ETHERNET ###
            # Adresse mac destination (=broadcast) :
            pack('!6B', *(0xFF,) * 6),
            # Adresse mac source :
            self.socket.getsockname()[4],
            # Type de protocole (=ARP) :
            pack('!H', 0x0806),

            ### Partie ARP ###
            # Type de protocole matériel/logiciel (=Ethernet/IP) :
            pack('!HHBB', 0x0001, 0x0800, 0x0006, 0x0004),
            # Type d'opération (=ARP Request) :
            pack('!H', 0x0001),
            # Adresse matériel de l'émetteur :
            self.socket.getsockname()[4],
            # Adresse logicielle de l'émetteur :
            saddr,
            # Adresse matérielle de la cible (=00*6) :
            pack('!6B', *(0,) * 6),
            # Adresse logicielle de la cible (=adresse fournie au
            # constructeur) :
            pack('!4B', *[int(x) for x in self.ipaddr.split('.')])
        ]

        self.socket.send(''.join(frame)) # Envois de la trame sur le
        # réseau


    def _wait_response(self):
        '''Attend la réponse de la machine'''

        t_begin = t_last_arp_sent = time.time()

        while True:

            now = time.time()
            if now - t_begin > self.timeout:
                return

            if now - t_last_arp_sent > self.arp_resend:
                self._send_arp_request()
                t_last_arp_sent = now

            # Récupération de la trame :
            frame = self.socket.recv(1024)

            # Récupération du protocole sous forme d'entier :
            proto_type = val2int(unpack('!2s', frame[12:14])[0])
            if proto_type != 0x0806: # On passe le traitement si ce
                continue             # n'est pas de l'arp


            # Récupération du type d'opération sous forme d'entier :
            op = val2int(unpack('!2s', frame[20:22])[0])
            if op != 2:  # On passe le traitement pour tout ce qui n'est
                continue # pas une réponse ARP

            # Récupération des différentes addresses de la trame :
            arp_headers = frame[18:20]
            arp_headers_values = unpack('!1s1s', arp_headers)
            hw_size, pt_size = [val2int(v) for v in arp_headers_values]
            total_addresses_byte = hw_size * 2 + pt_size * 2
            arp_addrs = frame[22:22 + total_addresses_byte]
            src_hw, src_pt, dst_hw, dst_pt = unpack('!%ss%ss%ss%ss'
                    % (hw_size, pt_size, hw_size, pt_size), arp_addrs)

            # Comparaison de l'adresse recherchée avec l'adresse trouvée
            # dans la trame :
            if src_pt == pack('!4B',
                             *[int(x) for x in self.ipaddr.split('.')]):
                # we got it
                return src_hw, src_pt, dst_hw, dst_pt

#############################################################################

class Plugin(BasePlugin):
    NAME = 'check-arp-no-change'
    VERSION = '0.1'
    DESCRIPTION = "Verify that a host MAC address hasn't changed"
    AUTHOR = 'Grégory Starck'
    EMAIL = 'gregory.starck@savoirfairelinux.com'
    
    ARGS = [
        ('h', 'help', 'display plugin help', False),
        ('v', 'version', 'display plugin version number', False),
        # Hammer time^W^W Add your plugin arguments here:
        # ('short', 'long', 'description', 'does it expect a value?')
        ('H', 'host', 'The host to check', True),
        #('m', 'mac', 'The MAC address the host should have', True),
        #('c', 'critical', "If ARP doesn't match then return a warning ; default is to return a warning.", False),
        #('w', 'warn-on-not-found', "If ARP isn't found (timeout) then force a warning return.", False),
        ('i', 'if_name', 'Specify the interface name to send ARP request. default='+DEFAULT_IFNAME, False),
    ]
    
    def check_args(self, args):
        host = args.get('host')
        mac = args.get('mac')
        args['if_name'] = args.get('if_name', DEFAULT_IFNAME)
        if not (host and mac):
            self.unknown('Host and MAC argument are required.')
        args['mac'] = mac.lower()
        return True, None

    def run2(self, host, mac, if_name='eth0', **kw):
        r = arprequest.ArpRequest(host, if_name=if_name)
        response = r.request()
        if response:
            src_hw, src_pt, dst_hw, dst_pt = response
            src_hw = ':'.join([b.encode('hex') for b in src_hw])
            if src_hw != mac:
                self.critical("MAC address for host %s = %s doesn't match the expected one (%s)" % (
                    host, src_hw, mac))
        else:
            self.warning('ARP address not found for host %s' % host)

    def run(self, args):
        self.run2(**args)
        self.ok('OK given MAC address corresponds to host')

if __name__ == "__main__":
    Plugin()