package Devel::Cover::Report::Clover::Project;
use strict;
use warnings;
use base qw(Devel::Cover::Report::Clover::Reportable);

sub report {
    my ($self) = @_;

    my @p_reports = map { $_->report } sort { $a->name cmp $b->name } @{ $self->packages };

    my $data = {
        name     => $self->name(),
        metrics  => $self->metrics(),
        packages => \@p_reports,
    };
    return $data;
}

sub metrics {
    my ($self) = @_;

    my $metrics = $self->SUPER::metrics();
    $metrics->{packages} = scalar @{ $self->packages };
    $metrics->{files}    = scalar @{ $self->files };
    $metrics->{classes}  = scalar @{ $self->classes };

    return $metrics;
}

sub classes {
    my ($self) = @_;
    return $self->builder->file_registry->classes;
}

sub packages {
    my ($self) = @_;
    return $self->builder->file_registry->packages;

}

sub package {
    my ( $self, $name ) = @_;
    $name = '' if !defined $name;
    my @found = grep { $_->name eq $name } @{ $self->packages };
    return undef unless @found;
    return $found[0];
}

sub files {
    my ($self) = @_;
    return $self->builder->file_registry->files;
}

sub summarize {
    my ($self) = @_;

    my $db = $self->builder->db;
    if ( !$db ) {
        return {};
    }

    my $summary = $db->summary('Total');
    if ( !$summary ) {
        return {};
    }

    my %s = %{$summary};

    my @criteria = $self->builder->accept_criteria();

    my %filtered;
    foreach my $c (@criteria) {
        next unless exists $s{$c};
        $filtered{$c} = $s{$c};
    }
    return \%filtered;
}

sub loc {
    my ($self) = @_;
    my $loc = 0;
    foreach my $f ( @{ $self->files } ) {
        $loc += $f->loc();
    }
    return $loc;
}

sub ncloc {
    my ($self) = @_;
    my $ncloc = 0;
    foreach my $f ( @{ $self->files } ) {
        $ncloc += $f->ncloc();
    }
    return $ncloc;
}

1;

