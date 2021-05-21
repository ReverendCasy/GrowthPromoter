#!/usr/bin/env python3

from Bio import SeqIO
from typing import Generator

import click
import os
import pandas as pd

"""
Extracts quary sequences present or absent in the given BLAST tabular output
"""

def extractPresent(seqs: Generator, tab: pd.core.frame.DataFrame) -> list:
    output = list()
    for seq in seqs:
        if seq.id in tab.iloc[:, 0].tolist():
            output.append(seq)

    return output


def extractAbsent(seqs: Generator, tab: pd.core.frame.DataFrame) -> list:
    output = list()
    for seq in seqs:
        if seq.id not in tab.iloc[:, 0].tolist():
            output.append(seq)

    return output


@click.command()
@click.option('--sequences', '-s', help='Specify an input sequence file', type=click.Path(exists=True))
@click.option('--table', '-t', help='''Specify an input BLAST result file in tabular format
(Query ID column must go first)''',
 type=click.Path(exists=True))
@click.option('--output', '-o', help='Specify an output file', type=click.Path(exists=False))
@click.option('--mode', '-m', help='''Specify whether records present or absent in the
BLAST results should be extracted. Options are: "pre", "abs" (default is "abs")''',
type=click.Choice(['abs', 'pre'], case_sensitive=False), default='abs')


def main(sequences, table, output, mode):
    with open(table, 'r') as handle:
        blast_res = pd.read_csv(handle, sep='\t', header=None, index_col=False)
        with open(sequences, 'r') as handle2:
            seqs = SeqIO.parse(handle2, 'fasta')
            if mode == 'pre':
                result = extractPresent(seqs, blast_res)
            elif mode == 'abs':
                result = extractAbsent(seqs, blast_res)
    with open(output, 'w') as handle:
        SeqIO.write(result, output, 'fasta')


if __name__ == '__main__':
    main()
