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

from shinkenplugins.plugin import ShinkenPlugin


class CheckRabbitmq(ShinkenPlugin):
    NAME = 'rabbitmq'
    VERSION = '1.0'
    DESCRIPTION = 'Verify good behavior of a RabbitMQ exchange and queue'
    AUTHOR = 'Grégory Starck'
    EMAIL = 'g.starck@gmail.com'

    DEFAULT_KEY_NAME = "RabbitMqPlugin"
    DEFAULT_KEY_VALUE = "42"

    DEFAULT_RABBITMQ_HOST = '127.0.0.1'
    DEFAULT_RABBITMQ_PORT = 5672

    DEFAULT_RABBITMQ_USER = 'guest'
    DEFAULT_RABBITMQ_PASSWORD = 'guest'

    DEFAULT_RABBITMQ_ROUTING_KEY = ''
    DEFAULT_RABBITMQ_EXCHANGE = 'monitoring.exchange.x'
    DEFAULT_RABBITMQ_QUEUE = 'monitoring.queue.q'

    DEFAULT_RABBITMQ_BODY = 'test body'
    DEFAULT_RABBITMQ_BODY_ENCODING = 'UTF-8'

    def __init__(self):
        super(CheckRabbitmq, self).__init__()
        self.add_warning_critical(
                {'help': "The maximum time to receive the message in the output queue after which "
                         "we consider a WARNING result.",
                 'default': 3},
                {'help': "The maximum time to receive the message in the output queue after which "
                         "we consider a CRITICAL result.",
                 'default': 10},
        )
        add = self.parser.add_argument
        add('--hostname', '-H', default=self.DEFAULT_RABBITMQ_HOST,
            help='The hostname where the RabbitMQ server is running.')
        add('--port', '-P', default=self.DEFAULT_RABBITMQ_PORT, type=int,
            help='The port where the RabbitMQ server is running.')
        add('--user', '-u', default=self.DEFAULT_RABBITMQ_USER,
            help='The user to use to authenticate.')
        add('--password', '-p', default=self.DEFAULT_RABBITMQ_PASSWORD,
            help='The password to use to authenticate.')
        add('--exchange', '-e', default=self.DEFAULT_RABBITMQ_EXCHANGE,
            help='The exchange to send a message to.')
        add('--routing-key', '-r', default=self.DEFAULT_RABBITMQ_ROUTING_KEY)
        add('--queue', '-q', default=self.DEFAULT_RABBITMQ_QUEUE,
            help='The queue where the message should arrive.')
        add('--body', '-b', default=self.DEFAULT_RABBITMQ_BODY,
            help='The message to be actually sent in the body.')
        add('--encoding', default=self.DEFAULT_RABBITMQ_BODY_ENCODING,
            help='The encoding to use for the body message.')
        add('--key-name', default=self.DEFAULT_KEY_NAME,
            help='The default header key name to be used to recognize the message that will be '
                 'published.')
        add('--key-value', default=self.DEFAULT_KEY_VALUE,
            help='The default header value to be used to recognize the message that will be '
                 'published.')

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
        creds = pika.PlainCredentials(args.user, args.password)
        params = pika.ConnectionParameters(host=args.hostname, port=args.port,
                                           credentials=creds, socket_timeout=1 + args.critical)

        conn = pika.BlockingConnection(parameters=params)
        channel = conn.channel()

        generated_uuid = uuid.uuid4()
        str_generated_uuid = str(generated_uuid)

        properties = pika.BasicProperties(
                content_encoding=args.encoding,
                headers={'uuid': str_generated_uuid,
                         args.key_name: args.key_value})

        gotit = []

        def callback(channel, method, properties, body):
            # print(channel, method, properties, body)
            if properties.headers and properties.headers.get('uuid') == str_generated_uuid:
                gotit.append(time.time())
                channel.basic_ack(method.delivery_tag)
                conn.remove_timeout(timeout_id)
                channel.stop_consuming()

        consumer_tag = channel.basic_consume(callback, args.queue,
                                             no_ack=False, exclusive=True)
        del consumer_tag  # unused

        t_published = time.time()
        channel.publish(args.exchange, args.routing_key, args.body.encode(args.encoding),
                        mandatory=True, properties=properties)

        # automatically stop consuming after args.critical + 1 seconds:
        timeout_id = conn.add_timeout(1 + args.critical, channel.stop_consuming)
        try:
            channel.start_consuming()
        except Exception as err:
            self.critical("Error while reading message from server: %s" % err)

        if gotit:
            t_received = gotit[0]
            elapsed = t_received - t_published
            str_elapsed = '%.3f sec (warn=%s crit=%s)' % (
                elapsed, args.warning, args.critical)
            if elapsed < args.warning:
                method = self.ok
            elif elapsed < args.critical:
                method = self.warning
            else:
                method = self.critical
            method(str_elapsed)
        else:
            self.critical("Timeout (%s) waiting message on %r queue ; Message lost ? "
                          "No consumer on the destination exchange %r ?" % (
                args.critical, args.queue, args.exchange))

############################################################################

Plugin = CheckRabbitmq

############################################################################


def main(argv=None):
    plugin = CheckRabbitmq()
    plugin.execute(argv)


if __name__ == "__main__":
    main()
