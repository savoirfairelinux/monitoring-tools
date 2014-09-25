#!/usr/bin/env python
#coding=utf8
#
# DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
# Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar
# 14 rue de Plaisance, 75014 Paris, France
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
# DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
# TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
# 0. You just DO WHAT THE FUCK YOU WANT TO.
#


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
