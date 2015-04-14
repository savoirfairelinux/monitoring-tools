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
    tdir = os.path.join(here, 'templates', args['type'])
    target = os.path.join(os.path.dirname(here), 'plugins', args['name'])
    
    if os.path.exists(target):
        print("The folder %s shouldn't exit" % target)
        sys.exit(1)

    exec_name = args['name'].replace('-', '_')
    short_name = exec_name.replace("check_", "")
    # we copy the needed files
    shutil.copytree(tdir, target, symlinks=True)
    

    shutil.move(os.path.join(target, 'debian', 'monitoring-plugins-sfl-check-foo.spec'),
                os.path.join(target, 'debian', 'monitoring-plugins-sfl-check-%s.spec' % short_name))

    shutil.move(os.path.join(target, 'shinkenplugins', 'plugins', 'foo'),
                os.path.join(target, 'shinkenplugins', 'plugins', short_name))

    shutil.move(os.path.join(target, 'shinkenplugins', 'plugins', short_name, 'foo.py'),
                os.path.join(target, 'shinkenplugins', 'plugins', short_name, '%s.py' % short_name))

    shutil.move(os.path.join(target, 'tests', 'test_check_foo.py'),
                os.path.join(target, 'tests', 'test_' + exec_name + '.py'))

    shutil.move(os.path.join(target, 'doc', 'plugin-check_foo.rst'),
                os.path.join(target, 'doc', 'plugin-' + exec_name + '.rst'))

    # and feed them to jinja2
    loader = FileSystemLoader(target)
    env = Environment(loader=loader)

    for k, v in args.items():
        if isinstance(v, type(b'')):
            args[k] = v.decode('utf8')


    # template variables
    tvars = dict(args)

    tvars['exec_name'] = args['name'].replace('-', '_')
    tvars['exec_name_capitalized'] = "".join([w.capitalize() for w in tvars['exec_name'].split("_")])
    tvars['short_name'] = short_name
    tvars['short_name_capitalized'] = "".join([w.capitalize() for w in short_name.split("_")])
    tvars['doc_name'] = "%s\n%s" % (tvars['exec_name'], "=" * len(tvars['exec_name']))
    now = datetime.now()
    tvars['year'] = now.year
    tvars['date_long'] = '%s.%s.%s.%s.%s' % (now.year, now.month, now.day, now.hour, now.minute)
    tvars['date_rpm'] = now.strftime("%a %b %d %Y")
    tvars['date_rfc2822'] = email.utils.formatdate(time.mktime(now.timetuple()))


    
    for template in env.list_templates():
        print template
        output = env.get_template(template).render(tvars)

        with codecs.open(os.path.join(target, template), 'w', 'utf8') as f:
            f.write(output)

    print('')
    print('Your plugin is ready!')
    print('You can now edit the files in plugin-%s' % args['name'])
    print('')
    print('main python executable: %s' % exec_name)
    print('tests suite:            test_%s.py' % exec_name)
    print('requirements:           requirements.txt, debian/control')
    print('')
    print('Good luck, and thanks for playing!')
    

def parse_args():
    parser = argparse.ArgumentParser(description='Create a new Shinken plugin.')
    required = [
        {'name': 'type', 'help': 'Type of plugin you want', 'choices': ['python',]},
        {'name': 'name',
         'help': 'The name of your plugin (should begin with check-, and use - instead of _)',
         'choices': None},
        {'name': 'desc', 'help': 'The description of your plugin', 'choices': None},
        {'name': 'author_name', 'help': 'Your name', 'choices': None},
        {'name': 'author_email', 'help': 'Your email address', 'choices': None},
        ]
    for arg in required:
        parser.add_argument('--' + arg['name'], help=arg['help'], choices=arg['choices'])

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
    
    return args

if __name__ == '__main__':
    args = parse_args()
    main(args)
