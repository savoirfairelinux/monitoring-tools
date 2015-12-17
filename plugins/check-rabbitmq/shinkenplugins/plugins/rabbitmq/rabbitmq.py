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

# Copyright (C) 2014, vdnguyen <vanduc.nguyen@savoirfairelinux.com>
#               2015, Grégory Starck <g.starck@gmail.com>


from __future__ import absolute_import

import time
import uuid

import pika

from shinkenplugins.perfdata import PerfData
from shinkenplugins.plugin import ShinkenPlugin


class CheckRabbitmq(ShinkenPlugin):
    NAME = 'rabbitmq'
    VERSION = '1.0'
    DESCRIPTION = 'Verify good behavior of a RabbitMQ exchange and queue'
    AUTHOR = 'Grégory Starck'
    EMAIL = 'g.starck@gmail.com'

    def __init__(self):
        super(CheckRabbitmq, self).__init__()
        self.add_warning_critical(
                {'help': "The maximum time to receive the message in the output queue after which "
                         "we consider a WARNING result.",
                 'default': 1},
                {'help': "The maximum time to receive the message in the output queue after which "
                         "we consider a CRITICAL result.",
                 'default': 3},
        )
        self.parser.add_argument('--hostname', '-H', default="127.0.0.1",
                                 help='The hostname where the RabbitMQ server is running.')
        self.parser.add_argument('--port', '-P', default=5672, type=int,
                                 help='The port where the RabbitMQ server is running.')
        self.parser.add_argument('--user', '-u', default="guest",
                                 help='The user to use to authenticate.')
        self.parser.add_argument('--password', '-p', default="guest",
                                 help='The password to use to authenticate.')
        self.parser.add_argument('--exchange', '-e', default="monitoring.exchange.x",
                                 help='The exchange to send a message to.')
        self.parser.add_argument('--routing-key', '-r', default="")
        self.parser.add_argument('--queue', '-q', default="monitoring.queue.q",
                                 help='The queue where the message should arrive.')
        self.parser.add_argument('--body', '-b', default="test body",
                                 help='The body to send in the message, will be encoded in UTF-8.')

    def parse_args(self, args):
        """ Use this function to handle complex conditions """
        args = super(CheckRabbitmq, self).parse_args(args)
        if None in (args.warning, args.critical):
            self.parser.error('--warning and --critical are both required.')
        if args.critical <= args.warning:
            self.parser.error('warning threshold must be strictly lower than critical one.')
        return args

    def run(self, args):
        """ Main Plugin function """
        encoding = 'UTF-8'
        creds = pika.PlainCredentials(args.user, args.password)
        params = pika.ConnectionParameters(host=args.hostname, port=args.port,
                                           credentials=creds, socket_timeout=1 + args.critical)

        conn = pika.BlockingConnection(parameters=params)
        channel = conn.channel()

        generated_uuid = uuid.uuid4()
        str_generated_uuid = str(generated_uuid)

        properties = pika.BasicProperties(
                content_encoding=encoding,
                headers={'uuid': str_generated_uuid,
                         'ShinkenRabbitMqPlugin': str(42)})
        # properties = None

        gotit = []

        def callback(channel, method, properties, body):
            # print(channel, method, properties, body)
            if properties.headers and properties.headers.get('uuid') == str_generated_uuid:
                gotit.append(time.time())
                channel.basic_ack(method.delivery_tag)
                conn.close()

        consumer_tag = channel.basic_consume(callback, args.queue,
                                             no_ack=False, exclusive=True)
        del consumer_tag  # unused

        t_publish = time.time()
        channel.publish(args.exchange, args.routing_key, args.body.encode(encoding),
                        mandatory=True, properties=properties)

        # automatically close the connection after args.critical + 1 seconds:
        conn.add_timeout(1 + args.critical, conn.close)
        try:
            channel.start_consuming()
        except Exception as err:
            self.critical("Error while reading message from server: %s" % err)

        if gotit:
            t_received = gotit[0]
            elapsed = t_publish - t_received
            if elapsed < args.warning:
                self.ok("OK")
            if elapsed < args.critical:
                self.warning("WARN")
            self.critical("DAMN")
        else:
            self.critical("Message lost ? No consumer on the destination exchange ?")

############################################################################

Plugin = CheckRabbitmq

############################################################################


def main(argv=None):
    plugin = CheckRabbitmq()
    plugin.execute(argv)


if __name__ == "__main__":
    main()
