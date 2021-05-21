#! /usr/bin/env python3

from Bio import SeqIO

import click

def checkLengths(file):
    tab = '\t'
    with open(file, 'r') as handle:
        for record in SeqIO.parse(handle, 'fasta'):
            print(f'{file.split("/")[-1]}{tab}{record.id}{tab}{len(record.seq)}')


@click.command()
@click.argument('input', type=click.Path(exists=True))

def execute(input):
    checkLengths(input)


if __name__ == '__main__':
    execute()

