#!/usr/bin/env python3

from collections import defaultdict
from itertools import chain
#from math import abs
from typing import TextIO

import click
import pandas as pd
import os

"""
Given a GFF file for the original genome sequence and an HMM output,
predicts whether any of the combinations of the plausible HMM results
satisfy the naive operon criteria
"""

def parseGff(gff: TextIO) -> pd.core.frame.DataFrame:
    """
    Parses a GFF file handle and returns a pandas dataframe
    """
    gff_df = pd.DataFrame(columns = ['Chromosome', 'Start', 'Stop', 'Strand'])
    col_nums = [0, 3, 4, 6]
    for line in gff:
        if line.find('#') == -1:
            line = line.split('\t')
            if line[2] == 'CDS':
                gff_df = gff_df.append(dict(zip(gff_df.columns , list(map(line.__getitem__, col_nums)))), ignore_index = True)
    return gff_df


def parseEggNOG(en: TextIO) -> pd.core.frame.DataFrame:
    """
    Parse EggNOG output and returns a pandas dataframe
    """
    pass


def parseHmm(hmm: TextIO) -> pd.core.frame.DataFrame:
    """
    Parse an HMMer output file and returns a pandas dataframe
    """
    hmm_df = pd.DataFrame(columns = ['Chromosome', 'Start', 'Stop', 'Strand', 
                                     'Cluster', 'eval_full', 'eval_b1d'])
    columns = [0, 2, 4, 7]
    for line in hmm:
        if line.find('#') < 0:
            line = line.split('\t')
            out = list(map(line.__getitem__, columns))
            out[0] = out[0].split(':')
            out[0][1] = out[0][1].split('-')
            out[1] = out[1].split('_')
            out[1] = f'{out[1][0]}_{out[1][2].split(".")[0]}'
            out = [out[0][0]] + out[0][1] + out[1:]
            strand = '+' if int(out[2]) > int(out[1]) else '-'
            out.insert(3, strand)
            hmm_df = hmm_df.append(dict(zip(hmm_df.columns, out)), ignore_index = True)
    return hmm_df


def parsePePPER(pep: TextIO) -> pd.core.frame.DataFrame:
    pass


@click.command()
@click.argument('gff', type=click.Path(exists=True), metavar='<PATH>')
@click.argument('hmm', type=click.Path(exists=True), metavar='PATH')
@click.option('--eggnog', '-en', help='''Provide an EggNOG output.
This will be used for KEGG pathway compliance estimation between operon members''',
type=click.Path(exists=True), metavar='<PATH>')
@click.option('--dthres', '-dt', help='''Physical distance threshold to allocate the genes 
to one operon''', type=int, metavar='<INT>', default = 1000)

def main(gff, hmm, eggnog, dthres):
#    operon_dict = defaultdict(lambda: defaultdict(list))
    operon_df = pd.DataFrame(columns = ['Replicon', 'Strand', 'Query', 'QueryStart', 
                                            'QueryStop', 'Subject', 'SubjectStart', 'SubjectStop',
                                             'Evidence'])
#    with open(gff, 'r') as handle:
#        gff_df = parseGff(handle)
#        click.echo(gff_df)
    with open(hmm, 'r') as handle:
        hmm_df = parseHmm(handle)
        hmm_df = hmm_df.astype({'Start': int, 'Stop':  int})
#        click.echo(hmm_df)
        for i in range(hmm_df.shape[0]):
            i_str = hmm_df.iloc[i].tolist()
#            i_name = '_'.join([i_str[4], str(i_str[1]), str(i_str[2]), i_str[0]])
            for j in range(i, hmm_df.shape[0]):
                j_str = hmm_df.iloc[j].tolist()
                if i_str[0] == j_str[0] and i_str[3] == j_str[3]:
                    if abs(i_str[1] - j_str[2]) < dthres or \
                       abs(j_str[1] - i_str[2]) < dthres:
#                        j_name = '_'.join([j_str[4], str(j_str[1]), str(j_str[2]), j_str[0]])
#                        operon_dict[i_name][j_name].append('Spatial evidence')
                        entry_line = [i_str[0], i_str[3], i_str[4], i_str[1], i_str[2],
                                      j_str[4], j_str[1], j_str[2], 'Spatial evidence']
                        operon_df = operon_df.append(dict(zip(operon_df.columns, entry_line)),
                                                     ignore_index = True)
    click.echo(operon_df)


if __name__ == '__main__':
    main()
