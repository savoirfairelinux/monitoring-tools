package Devel::Cover::Report::Clover;

use strict;
use warnings;

our $VERSION = "0.35";

use Devel::Cover::Report::Clover::Builder;
use Getopt::Long;

# Entry point which C<cover> uses
sub report {
    my ( $pkg, $db, $options ) = @_;

    my $report = builder( $db, $options );
    my $outfile = output_file($options);

    printf( "Writing clover output file to '%s'...\n", $outfile ) unless $options->{silent};
    $report->generate($outfile);

}

#extend the options for the C<cover> command line
sub get_options {
    my ( $self, $opt ) = @_;
    $opt->{option}{outputfile}  = "clover.xml";
    $opt->{option}{projectname} = "Devel::Cover::Report::Clover";
    die "Invalid command line options"
        unless GetOptions(
        $opt->{option},
        qw(
            outputfile=s
            projectname=s
            )
        );
}

sub output_file {
    my ($options) = @_;

    my $out_dir  = $options->{outputdir};
    my $out_file = $options->{option}{outputfile};
    my $out_path = sprintf( '%s/%s', $out_dir, $out_file );
    return $out_path;
}

sub builder {
    my ( $db, $options ) = @_;
    my $project_name = $options->{option}{projectname};
    my $report       = Devel::Cover::Report::Clover::Builder->new(
        {   db                         => $db,
            name                       => $project_name,
            include_condition_criteria => 1
        }
    );
}

1;

__END__

=head1 NAME

Devel::Cover::Report::Clover - Backend for Clover reporting of coverage statistics

=head1 SYNOPSIS

 cover -report clover

=head1 DESCRIPTION

This module generates a Clover compatible coverage xml file which can be used
in a variety of continuous integration software offerings.

It is designed to be called from the C<cover> program distributed with
L<Devel::Cover>.

=head1 OPTIONS

Options are specified by adding the appropriate flags to the C<cover> program.
This report format supports the following:

=over 4

=item outputfile

This will be the file name that you would like to write this report out to.
It defaults to F<clover.xml>.

=item projectname

This is simply a cosmetic item.  When the xml is generated, it has a project
name which will show up in your continuous integration system once it is
parsed.  This can be any string you want and it defaults to
'Devel::Cover::Report::Clover'.

=back

=head1 SEE ALSO

L<Devel::Cover>

L<http://www.atlassian.com/software/clover/>

L<http://jenkins-ci.org/>

L<https://wiki.jenkins-ci.org/display/JENKINS/Clover+Plugin>

=head1 BUGS

L<https://github.com/captin411/Devel-Cover-Report-Clover/issues>

=head1 CREDITS

Jun Kuriyama - nice cosmetic changes to package names

Olivier Mengué - fix tests for those using local::lib

=head1 AUTHOR

David Bartle <captindave@gmail.com>

=head1 LICENSE

Copyright David Bartle (captindave@gmail.com) 

This software is free.  It is licensed under the same terms as Perl itself.

The latest version of this software should be available on github.com
https://github.com/captin411/Devel-Cover-Report-Clover

=cut
