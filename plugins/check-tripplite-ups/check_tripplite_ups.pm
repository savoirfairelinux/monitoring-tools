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
#               <filename>.pm Check Trupplite UPSs
#
#
#     Author: Thibault Cohen <thibault.cohen@savoirfairelinux.com> 
#
#
 
use strict;
use warnings;
use sigtrap;
use diagnostics;

our $PLUGIN_NAME = "check_tripplite_ups";
our $PLUGIN_VERSION = "0.1";
our $TIMEOUT = 15;
our %ERRORS=('OK'=>0,'WARNING'=>1,'CRITICAL'=>2,'UNKNOWN'=>3,'DEPENDENT'=>4);

sub init() {
    use Getopt::Long;
    package check_tripplite_ups;
}

sub print_version() {
    my $version_msg = "
$PLUGIN_NAME.pl v$PLUGIN_VERSION (sfl-shinken-plugins)

The SFL Shinken Plugins come with ABSOLUTELY NO WARRANTY. You may redistribute
copies of the plugins under the terms of the GNU General Public License.
For more information about these matters, see the file named COPYING.
";
    print $version_msg;
}

sub print_support() {
    my $support_msg = "
Send email to thibault.cohen\@savoirfairelinux.com if you have questions
regarding use of this software. To submit patches or suggest improvements,
send email to thibault.cohen\@savoirfairelinux.com
Please include version information with all correspondence (when
possible, use output from the --version option of the plugin itself).
";
    print $support_msg;
}

sub print_usage() {
    my $usage_msg = "
$PLUGIN_NAME.pl -H <host> -w <warning> -c <critical>

Usage:
 -h, --help
    Print detailed help screen
 -H, --hostname=ADDRESS
    Host name, IP Address
 -V, --version
    Print version information
 -w, --warning=DOUBLE
    Response time to result in warning status (seconds)
 -c, --critical=DOUBLE
    Response time to result in critical status (seconds)
";
    print $usage_msg;
}

sub main() {
    init();
    my ($opt_v, $opt_h, $opt_C, $opt_V, $opt_H, $opt_w, $opt_c, $opt_t);
    my %args;

    $opt_C="public";
    $opt_V="2";
    $opt_H="";
    $opt_w="5";
    $opt_c="20";
    $opt_t="10";
     
    Getopt::Long::Configure('bundling');
    GetOptions(
        "v"   => \$args{"version"},     "version"     => \$args{"version"},
        "h"   => \$args{"help"},        "help"        => \$args{"help"},
        "C=s" => \$args{"community"},   "community"   => \$args{"community"},
        "V=s" => \$args{"snmpversion"}, "snmpversion" => \$args{"snmpversion"},
        "H=s" => \$args{"hostname"},    "hostname"    => \$args{"hostname"},
        "w=s" => \$args{"warning"},     "warning=s"   => \$args{"warning"},
        "c=s" => \$args{"critical"},    "critical=s"  => \$args{"critical"},
        "t=i" => \$args{"timeout"},     "timeout=i"   => \$args{"timeout"},
        );

    %args = check_arguments(%args);

    # Just in case of problems, let's not hang Nagios
    $SIG{'ALRM'} = sub {
        print "UNKNOWN - Plugin Timed out\n";
        exit $ERRORS{"UNKNOWN"};
    };
    alarm($args{"timeout"});
     
    if ($args{"version"}) {
        print_version();
        print_support();
        exit $ERRORS{'UNKNOWN'};
    }
     
    if ($args{"help"}) {
        print_version();
        print_usage();
        print_support();
        return $ERRORS{'UNKNOWN'};
    }

    get_data(%args);

}
    
sub check_arguments() {
    my %args = @_;

    if (! $args{"hostname"}) {
        print "Argument `hostname' is missing !\n";
        print_usage();
        exit $ERRORS{'UNKNOWN'};

    }

    if (! $args{"warning"}) {
        print "Argument `warning' is missing !\n";
        print_usage();
        exit $ERRORS{'UNKNOWN'};
    }

    if (! $args{"critical"}) {
        print "Argument `critical' is missing !\n";
        print_usage();
        exit $ERRORS{'UNKNOWN'};
    }

    if (! $args{"community"}) {
        $args{"community"} = "public";
    }

    if (! $args{"snmpversion"}) {
        $args{"snmpversion"} = "2c";
    }

    if (! $args{"timeout"}) {
        $args{"timeout"} = 10;
    }

    return %args
}
 

sub get_data() {
    my %args = @_;
    print "Given Options1:\n";
    printf ("Hostname: %s\n", $args{"hostname"});
    printf ("Community: %s\n", $args{"community"});
    printf ("SNMPVersion: %s\n", $args{"snmpversion"});
    printf ("Warning %s\n", $args{"warning"});
    printf ("Critical %s\n", $args{"critical"});
    printf ("Timeout %s\n", $args{"timeout"});

}


