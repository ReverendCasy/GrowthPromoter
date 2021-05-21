#!/usr/bin/env python3

from Bio import SeqIO
from typing import Generator

import os
import click

"""
Filters partial sequences from the FASTA file
"""

def filterPartial(source: Generator) -> tuple:
    complete, partials = [], []
    for item in source:
        if item.description.casefold().find('partial') == -1:
            complete.append(item)
        else:
            partials.append(item)

    return (complete, partials)

@click.command()
@click.option('--input', '-i', help='Path to an input file', type=click.Path(exists=True))
@click.option('--prefix', '-p', help='Specify a prefix for the output files', type=str, default='result')
@click.option('--output', '-o', help='Path to an output directory', type=click.Path(exists=False), default='.')

def main(input, prefix, output):
    with open(input, 'r') as handle:
        result = filterPartial(SeqIO.parse(handle, 'fasta'))
    complete_name, partial_name = f'{prefix}_complete.fasta', f'{prefix}_partial.fasta'
    SeqIO.write(result[0], os.path.join(output, complete_name), 'fasta')
    SeqIO.write(result[1], os.path.join(output, partial_name), 'fasta')

if __name__ == '__main__':
    main()
