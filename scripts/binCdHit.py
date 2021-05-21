#!/usr/bin/env python3

from Bio import SeqIO
from collections import defaultdict
from parseCdHit import parseCdHit
from typing import Generator

import click
import os

"""
Parses a CD-HIT '.clstr' file, then bins records from the original FASTA file according to the
clustering results and writes them to respective files
"""

def binCdHit(cdict: defaultdict, seqs: Generator) -> defaultdict:
    output = defaultdict(list)
    for seq in seqs:
        for key in cdict.keys():
            for sign in cdict[key]:
                if seq.description.find(sign) > -1:
                    output[key].append(seq)

    return output


@click.command()
@click.option('--clstr', '-c', help='Path to a clustering scheme file', type=click.Path(exists=True))
@click.option('--seqs', '-s', help='Path to the initial sequence file', type=click.Path(exists=True))
@click.option('--output', '-o', help='Path to an output directory', type=click.Path(exists=True))

def main(clstr, seqs, output):
    with open(clstr, 'r') as handle:
        cdict = parseCdHit(handle)
    with open(seqs, 'r') as handle:
        sequences = SeqIO.parse(handle, 'fasta')
        result = binCdHit(cdict, sequences)

    prefix = os.path.split(seqs)[1].split('.')[0]
    for key in result.keys():
        filename = f'{prefix}_cluster{key}.fasta'
        SeqIO.write(result[key], os.path.join(output, filename), 'fasta')


if __name__ == '__main__':
    main()
