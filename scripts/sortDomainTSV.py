#!/usr/bin/env python3

from typing import Generator

import click
import os
import pandas as pd

"""
Reorders an Interproscan output according to the domain order in each sequence
"""

def sortDomainTSV(tsv_gen = pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    return tsv_gen.sort_values(by = [0, 6, 7])


@click.command()
@click.argument('input', type=click.Path(exists=True), metavar='<PATH>')

def main(input):
    """
    Sorts an INPUT table from the Interproscan output in respect of domain order in each sequence
    """
    click.echo(sortDomainTSV(input))


if __name__ == '__main__':
    main()
