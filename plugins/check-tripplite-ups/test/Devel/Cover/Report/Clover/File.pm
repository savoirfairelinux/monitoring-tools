package Devel::Cover::Report::Clover::File;
use strict;
use warnings;
use base qw(Devel::Cover::Report::Clover::Reportable);

use overload '""' => \&to_string, fallback => 1;
use Devel::Cover::Report::Clover::Class;
use Devel::Cover::Report::Clover::Builder;
use File::Spec;

{
    my %Lines;

    sub lines {
        my ( $self, $optional_range ) = @_;

        if ( !defined $Lines{$self} ) {

            my $name = $self->name;
            my $db   = $self->builder->db;

            my $info = [];

            open( my $fh, '<', $name ) or warn("Can't read file '$name' [$!]\n"), return $info;
            my $cover_data = $db->cover->file($name);

            my ( $full_package, $class, $package, $line_no );

            my @lines;
        SOURCE_LINE:
            while ( my $sloc = <$fh> ) {
                chomp($sloc);
                my $line_no = $.;

                my $line_info = {
                    number   => $line_no,
                    type     => 'unknown',
                    content  => $sloc,
                    class    => $class ? $class : 'main',
                    package  => $package ? $package : '',
                    criteria => {},
                };

                if ( $sloc =~ /^\s*package\s+(.*)\s*;/ ) {
                    $full_package = $1;
                    my @parts = split /::/, $full_package;

                    $class = pop @parts;
                    $package = @parts ? join '::', @parts : '';

                    $line_info->{package} = $package;
                    $line_info->{class}   = $class;
                }

                if ( $sloc =~ /^__(END|DATA)__/ ) {
                    last SOURCE_LINE;
                }

                # Process embedded POD - yanked and tweaked from
                # Devel::Cover::Report::Html_minimal
                if ( $sloc =~ /^=(pod|head|over|item|begin|for)/ ) {

                    $line_info->{type} = 'pod';

                    push @lines, $line_info;
                POD_LOOP:
                    while ( my $line = <$fh> ) {
                        $line_no += 1;
                        chomp($line);
                        my %info = %{$line_info};
                        $info{content} = $line;
                        $info{number}  = $line_no;
                        push @lines, \%info;
                        last POD_LOOP if $line =~ /^=cut/;
                    }

                    next SOURCE_LINE;
                }

                if ( $sloc =~ /^\s*$/ ) {
                    $line_info->{type} = 'whitespace';
                    push @lines, $line_info;
                    next SOURCE_LINE;
                }

                if ( $sloc =~ /^\s*#/ ) {
                    $line_info->{type} = 'comment';
                    push @lines, $line_info;
                    next SOURCE_LINE;
                }

                my %criteria;
                for my $c ( $db->criteria ) {
                    next
                        unless grep { $c eq $_ }
                            Devel::Cover::Report::Clover::Builder->accept_criteria();
                    my $criterion = $cover_data->$c();
                    if ($criterion) {
                        my $l = $criterion->location($line_no);
                        next unless defined $l;
                        $criteria{$c} = $l ? [@$l] : $l;
                    }
                }

                $line_info->{type}     = 'code';
                $line_info->{criteria} = \%criteria;
                push @lines, $line_info;

            }

            close($fh);
            $Lines{$self} = \@lines;
        }

        if ($optional_range) {
            my @lines = @{ $Lines{$self} };
            return [ @lines[ $optional_range->[0] .. $optional_range->[1] ] ];
        }
        else {
            return $Lines{$self};
        }

    }
}

sub absolute_path {
    my ($self) = @_;
    return File::Spec->rel2abs( $self->name );
}

sub loc {
    my ( $self, $range ) = @_;

    my $lines = $self->lines($range);

    my $code_line_count = scalar grep { $_->{type} eq 'code' } @$lines;

    return scalar @$lines - $code_line_count;
}

sub ncloc {
    my ( $self, $range ) = @_;

    my $lines = scalar @{ $self->lines($range) };

    return $lines - $self->loc;
}

sub classes {
    my ( $self, $in_package ) = @_;

    my @classes;
    my $pl;
    my $line_number = 0;
    my $class_start = 1;
    my $flush_class = 0;

    my %classes;
    foreach my $l ( @{ $self->lines } ) {

        $line_number++;

        my $class_changed = defined $pl
            && ( $l->{package} ne $pl->{package}
            or $l->{class} ne $pl->{class} );

        if ($class_changed) {
            my $file_frag = Devel::Cover::Report::Clover::FileFragment->new(
                {   name       => $self->name,
                    builder    => $self->builder,
                    line_start => $class_start - 1,
                    line_end   => $line_number - 2,
                }
            );
            push @classes,
                Devel::Cover::Report::Clover::Class->new(
                {   file_fragment => $file_frag,
                    builder       => $self->builder,
                    name          => $pl->{class},
                    package       => $pl->{package}
                }
                );
            $class_start = $line_number;
            $flush_class = 0;
        }
        else {
            $flush_class = 1;
        }

        $pl = $l;

    }

    if ($flush_class) {
        my $file_frag = Devel::Cover::Report::Clover::FileFragment->new(
            {   name       => $self->name,
                builder    => $self->builder,
                line_start => $class_start - 1,
                line_end   => $line_number - 1,
            }
        );
        push @classes,
            Devel::Cover::Report::Clover::Class->new(
            {   file_fragment => $file_frag,
                builder       => $self->builder,
                name          => $pl->{class},
                package       => $pl->{package}
            }
            );
    }

    if ( defined $in_package ) {
        my @filtered = grep { $_->package eq $in_package } @classes;
        return \@filtered;
    }
    else {
        return \@classes;
    }

}

sub summarize {
    my ( $self, $range ) = @_;
    my $lines = $self->lines($range);

    my $accum = { summary => {} };
    my $key = 'accum';
    foreach my $line (@$lines) {
        my $criteria = $line->{criteria};
        next unless %$criteria;

        foreach my $criterion ( keys %$criteria ) {
            next
                unless grep { $criterion eq $_ }
                    Devel::Cover::Report::Clover::Builder->accept_criteria();
            my $items = $criteria->{$criterion};
            foreach my $item (@$items) {
                $item->calculate_summary( $accum, $key );
            }
            my $c = "Devel::Cover::\u$criterion";
            my $s = $accum->{summary}->{$key};
            my $t = $accum->{summary}->{Total};
            $c->calculate_percentage( $self, $s->{$criterion} );
            $c->calculate_percentage( $self, $s->{total} );
            $c->calculate_percentage( $self, $t->{$criterion} );
            $c->calculate_percentage( $self, $t->{total} );
        }
    }

    return $accum->{summary}->{Total};
}

sub to_string {
    return $_[0]->name;
}

1;

package Devel::Cover::Report::Clover::FileFragment;
use base qw(Devel::Cover::Report::Clover::File);
__PACKAGE__->mk_accessors(qw(line_start line_end package_limit));

sub classes {
    my ($self) = @_;
    return $self->SUPER::classes( $self->package_limit );
}

sub lines {
    my ($self) = @_;
    return $self->SUPER::lines( [ $self->line_start, $self->line_end ] );
}

1;

