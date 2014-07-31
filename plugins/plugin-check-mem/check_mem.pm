#!/usr/bin/perl -w
#
#
#     Original script :
#     check_mem Copyright (C) 2000 Justin Ellison <justin@techadvise.com>
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
#               check_mem.pm Plugin to check memory usage
#
#
#     check_mem Copyright (C) 2000 Dan Larsson <dl@tyfon.net>
#     Author: Justin Ellison <justin@techadvise.com>
#     Author: Thibault Cohen <thibault.cohen@savoirfairelinux.com> 
#
#

 
use strict;
use warnings;
use sigtrap;
use diagnostics;
use Getopt::Std;

our $PLUGIN_NAME = "check_mem";
our $PLUGIN_VERSION = "0.1";
our $TIMEOUT = 15;
our %ERRORS=('OK'=>0,'WARNING'=>1,'CRITICAL'=>2,'UNKNOWN'=>3,'DEPENDENT'=>4);

sub init() {
    use Getopt::Long;
    package check_mem;
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
$PLUGIN_NAME.pl -<f|u> -w <warning> -c <critical>

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
 -f, --free
    Check FREE memory
 -u, --used
    Check USED memory
 -C, --cache
    Count OS caches as FREE memory
 -v, --verbose
    Print more stuff
";
    print $usage_msg;
}

sub main() {
    init();
    my %args;

    Getopt::Long::Configure('bundling');
    GetOptions(
        "V"   => \$args{"version"},     "version"     => \$args{"version"},
        "h"   => \$args{"help"},        "help"        => \$args{"help"},
        "w=s" => \$args{"warning"},     "warning=s"   => \$args{"warning"},
        "c=s" => \$args{"critical"},    "critical=s"  => \$args{"critical"},
        "f"   => \$args{"free"},        "free"        => \$args{"free"},
        "u"   => \$args{"used"},        "used"        => \$args{"used"},
        "C"   => \$args{"cache"},       "cache"       => \$args{"cache"},
        "v"   => \$args{"verbose"},     "versbose"    => \$args{"verbose"},
        );

    %args = check_arguments(%args);

    # Just in case of problems, let's not hang Nagios
    $SIG{'ALRM'} = sub {
        print "UNKNOWN - Plugin Timed out\n";
        exit $ERRORS{"UNKNOWN"};
    };
    alarm(10);

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

    my ($free_memory_kb,$used_memory_kb,$caches_kb) = get_data(%args);
    print "$free_memory_kb Free\n$used_memory_kb Used\n$caches_kb Cache\n" if ($args{'verbose'});

    if ($args{"cache"}) { #Do we count caches as free?
        $used_memory_kb -= $caches_kb;
        $free_memory_kb += $caches_kb;
    }

    # Round to the nearest KB
    $free_memory_kb = sprintf('%d',$free_memory_kb);
    $used_memory_kb = sprintf('%d',$used_memory_kb);
    $caches_kb = sprintf('%d',$caches_kb);

    prepare_output($used_memory_kb,$free_memory_kb,$caches_kb,%args);

}
    
sub check_arguments() {
    my %args = @_;

    if (!$args{"warning"} or $args{"warning"} == 0 or !$args{"critical"} or $args{"critical"} == 0) {
        print "*** You must define WARN and CRITICAL levels!\n";
        print_usage();
        exit $ERRORS{'UNKNOWN'};
    }
    elsif (!$args{"free"} and !$args{"used"}) {
        print "*** You must select to monitor either USED or FREE memory!\n";
        print_usage();
        exit $ERRORS{'UNKNOWN'};
    }
    elsif ($args{"free"} and $args{"used"}) {
        print "*** You must select to monitor either USED or FREE memory!\n";
        print_usage();
        exit $ERRORS{'UNKNOWN'};
    }

    if ($args{"warning"} <= $args{"critical"} and $args{"free"}) {
        print "*** WARN level must not be less than CRITICAL when checking FREE memory!\n";
        exit $ERRORS{'UNKNOWN'};
    }

    if ($args{"warning"} >= $args{"critical"} and $args{"used"}) {
        print "*** WARN level must not be greater than CRITICAL when checking USED memory!\n";
        exit $ERRORS{'UNKNOWN'};
    }

    return %args
}

sub get_data {
    my %args = @_;

    my $used_memory_kb  = 0;
    my $free_memory_kb  = 0;
    my $total_memory_kb = 0;
    my $caches_kb       = 0;

    my $uname;
    if ( -e '/usr/bin/uname') {
        $uname = `/usr/bin/uname -a`;
    }
    elsif ( -e '/bin/uname') {
        $uname = `/bin/uname -a`;
    }
    else {
        die "Unable to find uname in /usr/bin or /bin!\n";
    }
    print "uname returns $uname" if ($args{'verbose'});
    if ( $uname =~ /Linux/ ) {
        my @meminfo = `/bin/cat /proc/meminfo`;
        foreach (@meminfo) {
            chomp;
            if (/^Mem(Total|Free):\s+(\d+) kB/) {
                my $counter_name = $1;
                if ($counter_name eq 'Free') {
                    $free_memory_kb = $2;
                }
                elsif ($counter_name eq 'Total') {
                    $total_memory_kb = $2;
                }
            }
            elsif (/^(Buffers|Cached):\s+(\d+) kB/) {
                $caches_kb += $2;
            }
        }
        $used_memory_kb = $total_memory_kb - $free_memory_kb;
    }
    elsif ( $uname =~ /SunOS/ ) {
        eval "use Sun::Solaris::Kstat";
        if ($@) { #Kstat not available
            if ($args{'cache'}) {
                print "You can't report on Solaris caches without Sun::Solaris::Kstat available!\n";
                exit $ERRORS{'UNKNOWN'};
            }
            my @vmstat = `/usr/bin/vmstat 1 2`;
            my $line;
            foreach (@vmstat) {
              chomp;
              $line = $_;
            }
            $free_memory_kb = (split(/ /,$line))[5] / 1024;
            my @prtconf = `/usr/sbin/prtconf`;
            foreach (@prtconf) {
                if (/^Memory size: (\d+) Megabytes/) {
                    $total_memory_kb = $1 * 1024;
                }
            }
            $used_memory_kb = $total_memory_kb - $free_memory_kb;

        }
        else { # We have kstat
            my $kstat = Sun::Solaris::Kstat->new();
            my $phys_pages = ${kstat}->{unix}->{0}->{system_pages}->{physmem};
            my $free_pages = ${kstat}->{unix}->{0}->{system_pages}->{freemem};
            # We probably should account for UFS caching here, but it's unclear
            # to me how to determine UFS's cache size.  There's inode_cache,
            # and maybe the physmem variable in the system_pages module??
            # In the real world, it looks to be so small as not to really matter,
            # so we don't grab it.  If someone can give me code that does this, 
            # I'd be glad to put it in.
            my $arc_size = (exists ${kstat}->{zfs} && ${kstat}->{zfs}->{0}->{arcstats}->{size}) ?
                 ${kstat}->{zfs}->{0}->{arcstats}->{size} / 1024
                 : 0;
            $caches_kb += $arc_size;
            my $pagesize = `pagesize`;

            $total_memory_kb = $phys_pages * $pagesize / 1024;
            $free_memory_kb = $free_pages * $pagesize / 1024;
            $used_memory_kb = $total_memory_kb - $free_memory_kb;
        }
    }
    elsif ( $uname =~ /AIX/ ) {
        my @meminfo = `/usr/bin/vmstat -v`;
        foreach (@meminfo) {
            chomp;
            if (/^\s*([0-9.]+)\s+(.*)/) {
                my $counter_name = $2;
                if ($counter_name eq 'memory pages') {
                    $total_memory_kb = $1*4;
                }
                if ($counter_name eq 'free pages') {
                    $free_memory_kb = $1*4;
                }
                if ($counter_name eq 'file pages') {
                    $caches_kb = $1*4;
                }
            }
        }
        $used_memory_kb = $total_memory_kb - $free_memory_kb;
    }
    else {
        if ($args{'cache'}) {
            print "You can't report on $uname caches!\n";
            exit $ERRORS{'UNKNOWN'};
        }
        my $command_line = `vmstat | tail -1 | awk '{print \$4,\$5}'`;
        chomp $command_line;
        my @memlist      = split(/ /, $command_line);

        # Define the calculating scalars
        $used_memory_kb  = $memlist[0]/1024;
        $free_memory_kb = $memlist[1]/1024;
        $total_memory_kb = $used_memory_kb + $free_memory_kb;
    }
    return ($free_memory_kb,$used_memory_kb,$caches_kb);
}

sub prepare_output {
    my ($used,$free,$caches,%args) = @_;

    # Calculate Total Memory
    my $total = $free + $used;
    print "$total Total\n" if ($args{'verbose'});

    my $warn = $args{'warning'} * $total / 100;
    my $crit = $args{'critical'} * $total / 100;

    my $perfdata;
    if ($args{'used'}) {
        $perfdata = "|TOTAL=${total}KB;;;0; USED=${used}KB;${warn};${crit};0;${total} FREE=${free}KB;;;0;${total} CACHES=${caches}KB;;;0;${total}";
    }
    elsif ($args{'free'}) {
        $perfdata = "|TOTAL=${total}KB;;;0; USED=${used}KB;;;0;${total} FREE=${free}KB;${warn};${crit};0;${total} CACHES=${caches}KB;;;0;${total}";
    }

    if ($args{'free'}) {
      my $percent = sprintf "%.1f", ($free / $total * 100);
      if ($percent <= $args{'critical'}) {
          finish("CRITICAL - $percent% ($free kB) free!$perfdata",$ERRORS{'CRITICAL'});
      }
      elsif ($percent <= $args{'warning'}) {
          finish("WARNING - $percent% ($free kB) free!$perfdata",$ERRORS{'WARNING'});
      }
      else {
          finish("OK - $percent% ($free kB) free.$perfdata",$ERRORS{'OK'});
      }
    }
    elsif ($args{'used'}) {
      my $percent    = sprintf "%.1f", ($used / $total * 100);
      if ($percent >= $args{'critical'}) {
          finish("CRITICAL - $percent% ($used kB) used!$perfdata",$ERRORS{'CRITICAL'});
      }
      elsif ($percent >= $args{'warning'}) {
          finish("WARNING - $percent% ($used kB) used!$perfdata",$ERRORS{'WARNING'});
      }
      else {
          finish("OK - $percent% ($used kB) used.$perfdata",$ERRORS{'OK'});
      }
    }
}

sub finish {
    my ($msg,$state) = @_;
    print "$msg\n";
    exit $state;
}
