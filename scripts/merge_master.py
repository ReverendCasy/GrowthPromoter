#!/usr/bin/env python3

from Bio import SeqIO
from collections import deque
from compareDomainLayout import checkDomainHomogeneity, compareDomainLayout
from sortDomainTSV import sortDomainTSV

import click
import os
import pandas as pd
import queue

"""
Effectively merges the cluster sequence files within a directory
"""


@click.command()
@click.option('--tabledir', '-t', type=click.Path(exists=True), metavar='<PATH>')
@click.option('--fastadir', '-f', type=click.Path(exists=True), metavar='<PATH>')


def main(tabledir, fastadir):
    tables = os.listdir(tabledir)

    fastas = os.listdir(fastadir)

    prefices = set(map(lambda x: x.split('_')[0], tables))
    for prefix in prefices:
        if not os.path.exists(os.path.join('tmp_tables', prefix)):
            os.makedirs(os.path.join('tmp_tables', prefix))
        filequeue = deque()
        counter = 1
        for table in tables:
            if table.find(prefix) > -1:
                filequeue.append(table)
        """
        For each two files, sort them, perform homogeneity check,
        and check whether they can be merged
        """
        while len(filequeue) > 1:
            first = filequeue.pop()
            counter = 0
            if os.path.getsize(os.path.join(tabledir, first)) > 0:
                tsv1 = pd.read_csv(os.path.join(tabledir, first), header=None, sep='\t')
                if checkDomainHomogeneity(tsv1):
                    while counter < len(filequeue):
                        second = filequeue.pop()
                        if os.path.getsize(os.path.join(tabledir, second)) > 0:
                            tsv2 = pd.read_csv(os.path.join(tabledir, second), header=None, sep= '\t')
                            if checkDomainHomogeneity(tsv2):
                                if compareDomainLayout(tsv1, tsv2):
                                    clust1, clust2 = first.split('.')[0].split('cluster')[1], \
                                                     second.split('.')[0].split('cluster')[1]
                                    new_name = f'{"_".join(first.split("_")[:-1])}_cluster{clust1}n{clust2}.fasta.tsv'
                                    print(new_name)
                                    new_tsv = tsv1.append(tsv2, ignore_index=True)
                                    with open(os.path.join(tabledir, new_name), 'w') as handle:
                                        new_tsv.to_csv(handle, header=False, index=False, sep='\t')
                                    os.remove(os.path.join(tabledir, first))
                                    os.remove(os.path.join(tabledir, second))
                                    filequeue.appendleft(new_name)
                                    fasta1, fasta2 = first.rstrip('.tsv'), second.rstrip('.tsv')
                                    new_fasta = new_name.rstrip('.tsv')
                                    with open(os.path.join(fastadir, new_fasta), 'w') as handle:
                                        for f2merge in (fasta1, fasta2):
                                            with open(os.path.join(fastadir, f2merge), 'r') as handle1:
                                                for line in handle1:
                                                    handle.write(line)
                                    fastas.append(new_fasta)
                                    os.remove(os.path.join(fastadir, fasta1))
                                    os.remove(os.path.join(fastadir, fasta2))
                                    break
                                else:
                                    filequeue.appendleft(second)
                                    counter += 1
                            else:
                                continue
                        else:
                            print(f'{second}is empty; removing')
                            t2rem = os.path.join(tabledir, second)
                            f2rem = os.path.join(fastadir, second.rstrip('.tsv'))
                            os.remove(t2rem)
                            os.remove(f2rem)
                else:
                    continue
            else:
                print(f'{first} is empty; removing')
                t2rem = os.path.join(tabledir, first)
                f2rem = os.path.join(fastadir, first.rstrip('.tsv'))
                os.remove(t2rem)
                os.remove(f2rem)


if __name__ == '__main__':
    main()
