#!/usr/bin/perl -w
#
#
#     Copyright (C) 2012 Savoir-Faire Linux Inc. 
#
#     This program is free software; you can redistribute it and/or modify 
#     it under the terms of the GNU General Public License as published by 
#     the Free Software Foundation; either version 3 of the License, or 
#     (at your option) any later version. 
#
#     This program is distributed in the hope that it will be useful, 
#     but WITHOUT ANY WARRANTY; without even the implied warranty of 
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
#     GNU General Public License for more details. 
#
#     You should have received a copy of the GNU General Public License 
#     along with this program; if not, write to the Free Software 
#     Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA. 
#
#     Projects :
#               SFL Shinken plugins
#
#     File :
#               <filename>.t Check Trupplite UPSs
#
#
#     Author: Thibault Cohen <thibault.cohen@savoirfairelinux.com> 
#
#


# Prepare
use strict;
use Test::More tests => 2;
use Test::Output;
require "check_tripplite_ups.pm";

our $PLUGIN_NAME; 
our $PLUGIN_VERSION; 

# Test version
my $expected = ".*$PLUGIN_NAME\.pl v$PLUGIN_VERSION.*";
stdout_like(\&print_version, qr/$expected/, 'YEAH2');

# Test Usage
$expected = ".*$PLUGIN_NAME\.pl v$PLUGIN_VERSION.*";
stdout_like(\&print_usage, qr/.*v.*/, 'YEAH');
