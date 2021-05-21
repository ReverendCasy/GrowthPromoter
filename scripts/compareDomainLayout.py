#!/usr/bin/env python3

import click
import os
import pandas as pd

"""
Compares two domain layout tables from the Interproscan output; prompts the respective file merging
if the layout is identical, does nothing otherwise
"""

def checkDomainHomogeneity(tsv_gen: pd.core.frame.DataFrame) -> bool:
    """
    Checks if all the sequences in the table have an identical domain content and order
    """
    if len(tsv_gen) % tsv_gen.iloc[:, 0].nunique() > 0:
        return False
    elif tsv_gen.iloc[:, 0].value_counts().nunique() > 1:
        return False

    period = tsv_gen.iloc[:, 0].value_counts()[0]
    checklist = list(map(lambda x: tsv_gen.iloc[x : x + period, 5].tolist(), range(0, len(tsv_gen), period)))

    return all(el == checklist[0] for el in checklist)


def compareDomainLayout(tsv1: pd.core.frame.DataFrame, tsv2: pd.core.frame.DataFrame) -> bool:
    """
    Compares the domain layout between two files. 
    Sequences must have passed the domain structure homogeneity filter prior.
    """
    per1, per2 = tsv1.iloc[:, 0].value_counts()[0], \
                 tsv2.iloc[:, 0].value_counts()[0]
    return tsv1.iloc[0 : per1, 5].tolist() == tsv2.iloc[0 : per2, 5].tolist()


@click.command()
@click.argument('tsv1', type=click.Path(exists=True), metavar='<PATH>')
@click.argument('tsv2', type=click.Path(exists=True), metavar='<PATH>')

def main(tsv1, tsv2):
    """
    Compares TSV1 to TSV2 in terms of domain layout
    """
    tsv_1 = pd.read_csv(tsv1, header=None, sep='\t')
    tsv_2 = pd.read_csv(tsv2, header=None, sep='\t')

    if checkDomainHomogeneity(tsv1) and checkDomainHomogeneity(tsv2):
        out = '' if compareDomainLayout(tsv_1, tsv_2) else 'not'
        click.echo(f'''The sequences {tsv1} and {tsv2} are {out} identical in terms of
                        domain structure''')


if __name__ == '__main__':
    main()
