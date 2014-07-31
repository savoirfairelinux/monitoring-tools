package Devel::Cover::Report::Clover::Class;
use strict;
use warnings;
use base qw(Devel::Cover::Report::Clover::Reportable);
__PACKAGE__->mk_accessors(qw( name package file_fragment ));

sub full_name {
    my ($self) = @_;

    return join '::', grep {$_} ( $self->package, $self->name );
}

sub report {
    my ($self) = @_;

    my $name = $self->name() || '';
    ( my $name_dotted = $name ) =~ s/\W+/./g;

    my $data = {
        name        => $name,
        name_dotted => $name_dotted,
        metrics     => $self->metrics(),
    };
    return $data;
}

sub metrics {
    my ($self) = @_;
    return $self->SUPER::metrics();
}

sub loc {
    my ($self) = @_;
    return $self->file_fragment->loc();
}

sub ncloc {
    my ($self) = @_;
    return $self->file_fragment->ncloc();
}

sub summarize {
    my ($self) = @_;
    return $self->file_fragment->summarize();
}

1;

