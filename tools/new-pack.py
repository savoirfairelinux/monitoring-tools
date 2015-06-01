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

# Copyright (C) 2014, Savoir-faire Linux, Inc.

# Authors:
#   Matthieu Caneill <matthieu.caneill@savoirfairelinux.com>
#   Grégory Starck <gregory.starck@savoirfairelinux.com>
#   Thibault Cohen <thibault.cohen@savoirfairelinux.com>
#
#############################################################################

from __future__ import unicode_literals

import os
import sys
import argparse
import shutil
import email.utils
import time
import codecs
from datetime import datetime


from jinja2 import Environment, FileSystemLoader


def main(args):
    here = os.path.dirname(os.path.abspath(__file__))
    tdir = os.path.join(here, 'templates', 'pack')
    target = os.path.join(os.path.dirname(here), 'packs', args['name'])
    
    if os.path.exists(target) and not args['update']:
        print("The folder %s shouldn't exit" % target)
        print("Or maybe you want to migrate with the last template version")
        sys.exit(1)
    if args['update'] and not os.path.exists(target):
        print("You want to update a pack and the folder %s doesn't exit" % target)
        sys.exit(1)

    # we copy the needed files
    if not args['update']:
        shutil.copytree(tdir, target, symlinks=True)
    else:
        file_ignored = ['commands.cfg', 'templates.cfg']
        for path, folders, files in os.walk(tdir):
            current_relative_folder = path.replace(tdir, "").strip("/")
            for file_ in files:
                if file_ not in file_ignored:
                    shutil.copy(os.path.join(path, file_),
                                os.path.join(target, current_relative_folder, file_))

    shutil.move(os.path.join(target,'debian', 'monitoring-packs-sfl-foo.spec'),
                os.path.join(target,'debian', 'monitoring-packs-sfl-' +  args['name'] + '.spec'))


    if not args['update']:
        shutil.move(os.path.join(target, 'pack', 'foo.pack'),
                os.path.join(target, 'pack', args['name'] + '.pack'))
        shutil.move(os.path.join(target, 'doc', 'foo.rst'),
                    os.path.join(target, 'doc', args['name'] + '.rst'))
    else:
        os.remove(os.path.join(target, 'doc', 'foo.rst'))
        os.remove(os.path.join(target, 'pack', 'foo.pack'))
        os.remove(os.path.join(target, 'pack', 'services', 'service1.cfg'))
        os.remove(os.path.join(target, 'pack', 'services', 'service2.cfg'))
 
    # and feed them to jinja2
    loader = FileSystemLoader(target)
    env = Environment(loader=loader)

    for k, v in args.items():
        if isinstance(v, type(b'')):
            args[k] = v.decode('utf8')

    args['tags'] = ",".join(['"%s"' % tag for tag in args['tags'].split(",")])
    # template variables
    tvars = dict(args)

    tvars['doc_name'] = "sfl-%s\n%s" % (tvars['name'], "=" * (len(tvars['name']) + 4))
    now = datetime.now()
    tvars['year'] = now.year
    tvars['date_long'] = '%s.%s.%s.%s.%s' % (now.year, now.month, now.day, now.hour, now.minute)
    tvars['date_rpm'] = now.strftime("%a %b %d %Y")
    tvars['date_rfc2822'] = email.utils.formatdate(time.mktime(now.timetuple()))

    for template in env.list_templates():
        print template
        try:
            output = env.get_template(template).render(tvars)
        except Exception as exp:
            print template, ": Can't be processed. Error :", exp
            continue
        with codecs.open(os.path.join(target, template), 'w', 'utf8') as f:
            f.write(output)

    print('')
    print('Your pack is ready!')
    print('You can now edit the files in packs/%(name)s' % args)
    print('')
    print('main template file: packs/%(name)s/pack/templates.cfg' % args)
    print('services template files: packs/%(name)s/pack/services/*' % args)
    print('')
    print('Good luck, and thanks for playing!')
    

def parse_args():
    parser = argparse.ArgumentParser(description='Create a new Shinken pack.')
    required = [
        {'name': 'system', 'help': 'Type of pack you want', 'choices': ['generic', 'linux', 'windows', 'vmware']},
        {'name': 'application', 'help': 'Application name you want monitor', 'choices': None},
        {'name': 'protocol', 'help': 'Protocol used in this new pack', 'choices': None},
        {'name': 'desc', 'help': 'The description of your pack', 'choices': None},
        {'name': 'tags', 'help': 'Pack tag list (comma separed)', 'choices': None},
        ]
    for arg in required:
        parser.add_argument('--' + arg['name'], help=arg['help'], choices=arg['choices'])

    parser.add_argument('--author_name', help='Your name', default='Savoir-faire Linux')
    parser.add_argument('--author_email', help='Your email address', default='supervision@savoirfairelinux.com')
    parser.add_argument('--update', help='Update', default=False, action='store_true')

    args = vars(parser.parse_args())

    for arg in required:
        if args[arg['name']] is None:
            msg = arg['help']
            if arg['choices']:
                msg += ' (' + '/'.join(arg['choices']) + ')'
            msg += ': '
            while True:
                resp = raw_input(msg)
                if arg['choices'] is None or resp in arg['choices']:
                    break
            args[arg['name']] = resp

    if args['application'] == args['protocol']:
        args['name'] = "%(system)s-%(application)s" % args
    else:
        args['name'] = "%(system)s-%(application)s-%(protocol)s" % args
    msg = "Your new pack will be named: %(name)s\nCorrect ? (y/n) " % args
    while True:
        resp = raw_input(msg)
        if resp == 'y':
            break
        elif resp == 'n':
            sys.exit(1)


    return args

if __name__ == '__main__':
    args = parse_args()
    main(args)
