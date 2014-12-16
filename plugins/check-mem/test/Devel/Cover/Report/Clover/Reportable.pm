package Devel::Cover::Report::Clover::Reportable;
use strict;
use warnings;
use base qw(Class::Accessor);
__PACKAGE__->mk_accessors(qw(builder name));

sub report {
    die("subclass must implement");
}

sub summarize {
    die("subclass must implement");
}

sub metrics {
    my $self = shift;

    my $s                    = $self->summarize();
    my $conditionals         = $s->{branch}->{total} || 0;
    my $conditionals_covered = $s->{branch}->{covered} || 0;
    if ( $self->builder->include_condition_criteria ) {
        $conditionals         += $s->{condition}->{total}   || 0;
        $conditionals_covered += $s->{condition}->{covered} || 0;
    }

    my $statements         = $s->{statement}->{total}   || 0;
    my $statements_covered = $s->{statement}->{covered} || 0;

    my $subroutines         = $s->{subroutine}->{total}   || 0;
    my $subroutines_covered = $s->{subroutine}->{covered} || 0;

    my $total         = $conditionals + $statements + $subroutines;
    my $total_covered = $conditionals_covered + $statements_covered + $subroutines_covered;

    my $metrics = {
        elements            => $total,
        coveredelements     => $total_covered,
        statements          => $statements,
        coveredstatements   => $statements_covered,
        complexity          => 0,
        loc                 => $self->loc(),
        ncloc               => $self->ncloc(),
        conditionals        => $conditionals,
        coveredconditionals => $conditionals_covered,
        methods             => $subroutines,
        coveredmethods      => $subroutines_covered
    };

    return $metrics;
}

1;
