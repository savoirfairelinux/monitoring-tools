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
#               check_mem.t Plugin to check memory usage
#
#
#     Author: Thibault Cohen <thibault.cohen@savoirfairelinux.com> 
#
#


# Prepare
use strict;
use Test::More tests => 15;
use Test::Output;
use Test::Trap;
require "check_mem.pm";

our $PLUGIN_NAME; 
our $PLUGIN_VERSION; 

# Test Version
my $res = trap { print_version() };
like( $trap->stdout, qr/.*$PLUGIN_NAME\.pl v$PLUGIN_VERSION.*/, "Test version");
# Test Usage
$res = trap { print_usage() };
like( $trap->stdout, qr/.*$PLUGIN_NAME\.pl -.*/, "Test usage");
# Test Support
$res = trap { print_support() };
like( $trap->stdout, qr/.*Send email to.*/, "Test support");

# Test bad arguments
my %args = (
"version" => 0,
"help" => 0,
"warning" => 80,
#"critical" => 90,
"free" => 0,
"used" => 1,
"cache" => 1,
"verbose" => 0,
);
my %res_args;
%res_args = trap { check_arguments(%args) };
is( $trap->exit, 3, 'Test bad arguments - Critical missing' );

# Test bad arguments FREE AND USED
%args = (
"version" => 0,
"help" => 0,
"warning" => 80,
"critical" => 90,
"free" => 1,
"used" => 1,
"cache" => 1,
"verbose" => 0,
);
%res_args = trap { check_arguments(%args) };
is( $trap->exit, 3, 'Test bad arguments - FREE AND USED set' );

# Test bad arguments NOT (FREE AND USED)
%args = (
"version" => 0,
"help" => 0,
"warning" => 80,
"critical" => 90,
"free" => 0,
"used" => 0,
"cache" => 1,
"verbose" => 0,
);
%res_args = trap { check_arguments(%args) };
is( $trap->exit, 3, 'Test bad arguments - FREE AND USED no set' );

# Test bad arguments FREE Warning > Critical
%args = (
"version" => 0,
"help" => 0,
"warning" => 80,
"critical" => 90,
"free" => 1,
"used" => 0,
"cache" => 1,
"verbose" => 0,
);
%res_args = trap { check_arguments(%args) };
is( $trap->exit, 3, 'Test bad arguments - FREE Warning > Critical' );

# Test bad arguments USED Warning < Critical
%args = (
"version" => 0,
"help" => 0,
"warning" => 90,
"critical" => 80,
"free" => 0,
"used" => 1,
"cache" => 1,
"verbose" => 0,
);
%res_args = trap { check_arguments(%args) };
is( $trap->exit, 3, 'Test bad argumentss - USED Warning < Critical' );

# Test check_arguments - USED
%args = (
"version" => 0,
"help" => 0,
"warning" => 80,
"critical" => 90,
"free" => 0,
"used" => 1,
"cache" => 1,
"verbose" => 0,
);
%res_args = trap { check_arguments(%args) };
is_deeply( \%res_args, \%args, "Test check_arguments function with good args");

# Test get data
my ($free_memory_kb,$used_memory_kb,$caches_kb) = get_data(%args);
ok($free_memory_kb, "Test get_data return");

# Test prepare output
my $traptrap = trap { prepare_output($free_memory_kb,$used_memory_kb,$caches_kb, %args) }; 
like( $trap->stdout, qr/.*|TOTAL.*/, "Test output");

# Test check_arguments - FREE
%args = (
"version" => 0,
"help" => 0,
"warning" => 20,
"critical" => 10,
"free" => 1,
"used" => 0,
"cache" => 1,
"verbose" => 0,
);
%res_args = trap { check_arguments(%args) };
is_deeply( \%res_args, \%args, "Test check_arguments function with good args");

# Test get data
($free_memory_kb,$used_memory_kb,$caches_kb) = get_data(%args);
ok($free_memory_kb, "Test get_data return");

# Test prepare output
$traptrap = trap { prepare_output($free_memory_kb,$used_memory_kb,$caches_kb, %args) };
like( $trap->stdout, qr/.*|TOTAL.*/, "Test output");

# Test main
$res = trap { main() };
is( $trap->exit, 3, 'Test main' );
