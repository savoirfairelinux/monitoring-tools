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
# Author:  Matthieu Caneill <matthieu.caneill@savoirfairelinux.com>

import os
import sys
import argparse
import shutil
import email.utils
import time
from datetime import datetime


from jinja2 import Environment, FileSystemLoader

def main(args):
    here = os.path.dirname(os.path.abspath(__file__))
    tdir = os.path.join(here, 'templates', args['type'])
    target = os.path.join(os.path.dirname(here), 'plugin-' + args['name'])
    
    if os.path.exists(target):
        print("The folder %s shouldn't exit" % target)
        sys.exit(1)

    exec_name = args['name'].replace('-', '_')
    # we copy the needed files
    shutil.copytree(tdir, target, symlinks=True)
    
    shutil.move(os.path.join(target, 'check_foo'),
                os.path.join(target, exec_name))
    
    shutil.move(os.path.join(target, 'test_check_foo.py'),
                os.path.join(target, 'test_' + exec_name + '.py'))
    
    os.symlink(exec_name,
               os.path.join(target, exec_name + '.py'))

    # and feed them to jinja2
    loader = FileSystemLoader(target)
    env = Environment(loader=loader)

    # template variables
    tvars = dict(args)

    tvars['exec_name'] = args['name'].replace('-', '_')
    now = datetime.now()
    tvars['year'] = now.year
    tvars['date_long'] = '%s.%s.%s.%s.%s' % (now.year, now.month, now.day, now.hour, now.minute)
    tvars['date_rfc2822'] = email.utils.formatdate(time.mktime(now.timetuple()))
    
    
    for template in env.list_templates():
        output = env.get_template(template).render(tvars)
        with open(os.path.join(target, template), 'w') as f:
            f.write(output)

    print('')
    print('Your plugin is ready!')
    print('You can now edit the files in plugin-%s' % args['name'])
    

def parse_args():
    parser = argparse.ArgumentParser(description='Create a new Shinken plugin.')
    required = [
        {'name': 'type', 'help': 'Type of plugin you want', 'choices': ['python', 'bash']},
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
