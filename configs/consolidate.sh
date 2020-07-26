#!/bin/bash

#PBS -l nodes=1:ppn=8,walltime=64:00:00,vmem=80gb
#PBS -j oe
#PBS -m abe
#PBS -d /N/slate/sialsaff/code4Rice3K/

module load java/1.8.0_131

./gatk GenomicsDBImport -R reference.fasta --sample-name-map accessions.sample_map --genomicsdb-workspace-path outputdir/ -L chr01 --consolidate --batch-size 50 --reader-thread 5 --create-output-variant-index --tmp-dir=tempdir/
