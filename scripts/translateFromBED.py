#!/usr/bin/env python3

from Bio import Seq
from Bio import SeqIO

import click
import pandas as pd
import os

@click.command()
@click.option('--bed', '-b', type=click.Path(exists=True))
@click.option('--fasta', '-f', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(exists=False))

def main(bed, fasta, output):
    with open(bed, 'r') as handle:
        table = pd.read_csv(handle, sep='\t', header=None)
#        seqs = ['_'.join(list(map(lambda x: str, table.iloc[i, :].tolist())))]
    with open(fasta, 'r') as handle:
        seqs = SeqIO.parse(handle, 'fasta')
        outlist = []
        for seq in seqs:
#            print(seq.id)
#            print(seq.id.split(':')[0], int(seq.id.replace(':', '-').split('-')[1]))
#            loc = table[(table.iloc[:, 0] == seq.id.split(':')[0]) & (str(table.iloc[:, 1]) == seq.id.replace(':', '-').split('-')[1])]
            loc = table[(table.iloc[:, 0] == seq.id.split(':')[0]) & (table.iloc[:, 1] == int(seq.id.replace(':', '-').split('-')[1]))]
#            print(loc[3].values[0])
            if loc[3].values[0] == '-':
                seq.seq = seq.seq.reverse_complement()
            seq.seq = seq.seq.translate(to_stop=True)
            outlist.append(seq)
#            for i in range(len(loc_table)):
#                if table.iloc[i, :3].tolist() == seq.id.replace('-', ':').split(':'):
#                    if table.iloc[i, 3] == '-':
#                        seq.seq = seq.seq.reverse_complement()
#                    seq.seq = seq.seq.translate(to_stop=True)
#                    outlist.append(seq)
    with open(output, 'w') as handle:
        SeqIO.write(outlist, handle, 'fasta')


if __name__ == '__main__':
    main()
