#!/bin/bash

#PBS -l nodes=1:ppn=4,walltime=36:00:00,vmem=30gb
#PBS -j oe
#PBS -m abe
#PBS -d /N/slate/sialsaff/code4Rice3K/

module load java/1.8.0_131 samtools

./gatk HaplotypeCaller -ERC GVCF -I accession.bam -R reference.fasta -O outputdir/accession.g.vcf.gz
