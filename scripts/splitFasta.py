#!/usr/bin/env python

"""
./splitFasta.py <reference.fasta> <chrom> > <out.fasta>
"""

from Bio import SeqIO
import sys

wantedSeqs = sys.argv[2]
seqs = SeqIO.parse(open(sys.argv[1]), 'fasta')
SeqIO.write((seq for seq in seqs if seq.id in wantedSeqs), sys.stdout, 'fasta')

