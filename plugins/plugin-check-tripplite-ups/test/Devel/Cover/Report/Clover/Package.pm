package Devel::Cover::Report::Clover::Package;
use strict;
use warnings;
use Devel::Cover::Criterion;
use base qw(Devel::Cover::Report::Clover::Reportable);
__PACKAGE__->mk_accessors(qw(classes));

sub report {
    my ($self) = @_;

    my $name = $self->name() || 'main';
    ( my $name_dotted = $name ) =~ s/\W+/./g;

    my $data = {
        name        => $name,
        name_dotted => $name_dotted,
        metrics     => $self->metrics(),
        files       => [ map { $_->report } @{ $self->files } ],
    };
    return $data;
}

sub files {
    my ($self) = @_;

    my %frag_classes;
    foreach my $c ( @{ $self->classes } ) {
        my $n = $c->file_fragment->name;
        push @{ $frag_classes{$n} }, $c;
    }

    my @ret;
    foreach my $name ( sort keys %frag_classes ) {
        my $classes = $frag_classes{$name};
        my $file    = Devel::Cover::Report::Clover::PackageFile->new(
            {   name    => $name,
                builder => $self->builder,
                classes => [@$classes]
            }
        );
        push @ret, $file;
    }

    return \@ret;

}

sub metrics {
    my ($self) = @_;

    my $metrics = $self->SUPER::metrics();
    $metrics->{files}   = scalar @{ $self->files };
    $metrics->{classes} = scalar @{ $self->classes() };

    return $metrics;
}

sub summarize {
    my ($self) = @_;
    my $classes = $self->classes();

    my $summary = {};

    foreach my $class (@$classes) {
        my $cs = $class->summarize();
        foreach my $criteria ( keys %$cs ) {
            my $cr = $cs->{$criteria};
            foreach my $data ( keys %$cr ) {
                $summary->{$criteria}->{$data} += $cs->{$criteria}->{$data};
            }
            Devel::Cover::Criterion->calculate_percentage( $self, $summary->{$criteria} );
        }
    }

    Devel::Cover::Criterion->calculate_percentage( $self, $summary->{total} );

    return $summary;

}

sub loc {
    my ($self) = @_;
    my $classes = $self->classes();

    my $loc = 0;
    foreach (@$classes) {
        $loc += $_->loc();
    }
    return $loc;
}

sub ncloc {
    my ($self) = @_;
    my $classes = $self->classes();

    my $ncloc = 0;
    foreach (@$classes) {
        $ncloc += $_->ncloc();
    }
    return $ncloc;
}

1;

package Devel::Cover::Report::Clover::PackageFile;
use strict;
use warnings;
use Devel::Cover::Criterion;
use base qw(Devel::Cover::Report::Clover::Reportable);
__PACKAGE__->mk_accessors(qw(classes));

sub report {
    my ($self) = @_;
    my $data = {
        name    => $self->name(),
        metrics => $self->metrics(),
        classes => [ map { $_->report } @{ $self->classes } ],
    };
    return $data;
}

sub metrics {
    my ($self) = @_;

    my $metrics = $self->SUPER::metrics();
    $metrics->{classes} = scalar @{ $self->classes() };
    return $metrics;
}

sub summarize {
    my ($self) = @_;
    my $classes = $self->classes;

    my $summary = {};

    foreach my $class (@$classes) {
        my $cs = $class->summarize();
        foreach my $criteria ( keys %$cs ) {
            my $cr = $cs->{$criteria};
            foreach my $data ( keys %$cr ) {
                $summary->{$criteria}->{$data} += $cs->{$criteria}->{$data};
            }
            Devel::Cover::Criterion->calculate_percentage( $self, $summary->{$criteria} );
        }
    }

    Devel::Cover::Criterion->calculate_percentage( $self, $summary->{total} );

    return $summary;

}

sub loc {
    my ($self) = @_;
    my $classes = $self->classes();

    my $loc = 0;
    foreach (@$classes) {
        $loc += $_->loc();
    }
    return $loc;
}

sub ncloc {
    my ($self) = @_;
    my $classes = $self->classes();

    my $ncloc = 0;
    foreach (@$classes) {
        $ncloc += $_->ncloc();
    }
    return $ncloc;
}

1;
1;
