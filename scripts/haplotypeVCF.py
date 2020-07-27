#!/usr/bin/env python3

"""
./haplotypeVCF.py <infile.vcf.gz>
"""

import sys
from cyvcf2 import VCF, Variant, Writer
import re
import numpy as np

vcf_file = sys.argv[1]

#vcf_file = "".join([name, '.vcf.gz'])
vcf = VCF(vcf_file)

sample = vcf.samples[0]
sample_a = ''.join([sample, '_a'])
sample_b = ''.join([sample, '_b'])

# Getting the vcf header
rawheader = vcf.raw_header
newline = "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t%s"

headerlist = []
for line in rawheader.split('\n'):
    if line.startswith('##'):
        headerlist.append(line)
    else:
        pass

headerlist.append(newline)
header = '\n'.join(map(str, headerlist))

w_a = Writer.from_string(''.join([sample, '_a.vcf.gz']), header % sample_a)
w_a.write_header()

w_b = Writer.from_string(''.join([sample, '_b.vcf.gz']), header % sample_b)
w_b.write_header()


for v in vcf:
    # class to get genotype in 0/0, 0/1, ... etc. format.
    gts = v.genotypes
    class Genotype(object):
        __slots__ = ('alleles', 'phased')

        def __init__(self, li):
            self.alleles = li[:-1]
            self.phased = li[-1]

        def __str__(self):
            sep = '/|'[int(self.phased)]
            return sep.join('0123.'[a] for a in self.alleles)
        __repr__ = __str__

    genotypes = [Genotype(li) for li in gts]
    #print(genotypes)
    
    #print(v.end, v.gt_bases)
    if v.gt_types == 0:
        ref, alt, gt_a, gt_b = v.REF, v.REF, "0/0", "0/0"
    elif v.gt_types == 1:
        ref, alt, gt_a, gt_b = re.split('/|\|', v.gt_bases[0])[0], re.split('/|\|', v.gt_bases[0])[1], "0/0", "1/1"
    elif v.gt_types == 3:
        ref, alt, gt_a, gt_b = re.split('/|\|', v.gt_bases[0])[0], re.split('/|\|', v.gt_bases[0])[1], "1/1", "1/1"
    elif v.gt_types == 2:
        ref, alt, gt_a, gt_b = ".", ".", "1/1", "1/1"
    else:
        raise ValueError("An unknown genotype encountered with gt_types!", v)

    Chr = v.CHROM
    Pos = v.end
    Id = v.ID
    Ref_nuc = ref
    Alt_nuc = alt
    Qual = np.round(v.QUAL, decimals=2)
    Filter = '.'
    Info = '.'
    Format = 'GT'
    gt_hom_ref = gt_a
    gt_hom_alt = gt_b

    #print(Chr, Pos, Id, Ref_nuc, Alt_nuc, Qual, Filter, Info, Format, gt_hom_ref, gt_hom_alt, sep='\t')

    v_a = w_a.variant_from_string('%s\t%d\t%s\t%s\t%s\t%d\t%s\t%s\t%s\t%s' % (Chr,Pos,Id,Ref_nuc,Alt_nuc,Qual,Filter,Info,Format,gt_hom_ref))
    v_b = w_b.variant_from_string('%s\t%d\t%s\t%s\t%s\t%d\t%s\t%s\t%s\t%s' % (Chr,Pos,Id,Ref_nuc,Alt_nuc,Qual,Filter,Info,Format,gt_hom_alt))
    w_a.write_record(v_a)
    w_b.write_record(v_b)
    
w_a.close()
w_b.close()

