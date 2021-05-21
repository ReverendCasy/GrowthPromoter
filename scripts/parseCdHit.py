#!/usr/bin/env python3

from collections import defaultdict
from typing import Generator

import click
import os

"""
Parses a CD-HIT '.clstr' output file and returns a dictionary 
mapping sequence signatures to cluster names
"""

def parseCdHit(cfile: Generator) -> defaultdict:
    output = defaultdict(list)
    for line in cfile:
        if line.find('>Cluster') > -1:
            current_key = line.split(' ')[1].rstrip('\n')
        else:
            current_value = line.split(', >')[1].split('...')[0]
            output[current_key].append(current_value)

    return output

@click.command()
@click.option('--input', '-i', help='Path to a .clstr file', type=click.Path(exists=True))

def main(input):
    with open(input, 'r') as handle:
        result = parseCdHit(handle)
    click.echo(result)


if __name__ == '__main__':
    main()
