#!/usr/bin/env python3

from Bio import SeqIO

import click
import os


@click.command()
@click.option('--seqdir', '-s', type=click.Path(exists=True), metavar='<path>')
@click.option('--cutperc', '-c', type=int, metavar='<int>', default=10)


def main(seqdir: click.Path, cutperc: int):

    """
    Removes cluster files containing less than 10% of the total amount of sequences
    """

    files = os.listdir(seqdir)
    patterns = set(map(lambda x: x.split('_')[0], files))
    for pattern in patterns:
        tmpdict = dict()
        all_seqs = 0
        for file in files:
            if file.find(pattern) > -1:
                with open(os.path.join(seqdir, file), 'r') as handle:
                    seqnum = 0
                    seqs = SeqIO.parse(handle, 'fasta')
                    for seq in seqs:
                        seqnum += 1
                    tmpdict[file] = seqnum
                    all_seqs += seqnum
        cutoff = round(all_seqs * (cutperc / 100))
        for key in tmpdict:
            if tmpdict[key] < cutoff:
                os.remove(os.path.join(seqdir, key))


if __name__ == '__main__':
    main()


