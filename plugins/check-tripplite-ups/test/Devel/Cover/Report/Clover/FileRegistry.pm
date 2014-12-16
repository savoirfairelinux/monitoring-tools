package Devel::Cover::Report::Clover::FileRegistry;
use strict;
use warnings;
use Devel::Cover::Report::Clover::File;
use Devel::Cover::Report::Clover::Package;
use base qw(Class::Accessor);
__PACKAGE__->mk_accessors(qw(builder files_table));

sub new {
    my $class = shift;
    my $self  = $class->SUPER::new(@_);

    my %files_table;
    foreach ( @{ $self->file_names } ) {
        $files_table{$_} = Devel::Cover::Report::Clover::File->new(
            {   builder => $self->builder,
                name    => $_
            }
        );
    }
    $self->files_table( \%files_table );
    return $self;
}

sub file_names {
    my ($self) = @_;
    my @files = $self->builder->db->cover->items;
    return \@files;
}

sub file {
    my ( $self, $file_name ) = @_;
    return $self->files_table->{$file_name};
}

sub files {
    my ($self) = @_;
    my @items = values %{ $self->files_table };
    return \@items;
}

sub classes {
    my ($self) = @_;
    my @classes = map { @{ $_->classes } } @{ $self->files };
    return \@classes;
}

sub packages {
    my ($self) = @_;
    my $classes = $self->classes();

    my %package_classes;
    foreach my $class (@$classes) {
        my $name = $class->package();
        push @{ $package_classes{$name} }, $class;
    }

    my @packages;
    foreach my $pname ( keys %package_classes ) {
        my $pcs     = $package_classes{$pname};
        my $package = Devel::Cover::Report::Clover::Package->new(
            {   name    => $pname,
                builder => $self->builder,
                classes => $pcs,
            }
        );
        push @packages, $package;
    }
    return \@packages;
}

1;
