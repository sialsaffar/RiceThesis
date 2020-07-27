#!/usr/bin/env python3

"""
./getAltFASTA.py <reference.fasta> <input.vcf.gz> <accession> <chrom> <output>
"""

import sys
from pyfaidx import Fasta, FastaVariant

fasta_file = sys.argv[1]
vcf_file = sys.argv[2]
sn = sys.argv[3]
chromosome = sys.argv[4]
out_file = ''.join([sn, '_alt.fasta'])

consensus = FastaVariant(fasta_file, vcf_file, sample=sn, het=False, hom=True, call_filter='GT == "1/1"')

with open(out_file, 'w') as outfile:
    print('>', sn, sep='', file=outfile)
    for line in consensus[chromosome]:
        print(line, file=outfile)
