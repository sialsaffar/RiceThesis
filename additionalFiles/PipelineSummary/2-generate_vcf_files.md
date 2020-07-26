
## Pipeline used for variants calling:

1. Run GATK's HaplotypeCaller on each accession BAM file to get GVCF files

    `./gatk HaplotypeCaller -ERC GVCF --input accession.bam --reference reference.fasta --output outputdir/accession.g.vcf.gz`

2. Merge GVCF files for each group into a genomics database

Note: The argument `--sample-name-map` takes a file containing a list of each accession name and the path to where that accession is located in a tab-delimited format. Each accession is separated by a new line.

    `./gatk GenomicsDBImport --reference reference.fasta --sample-name-map accessions.sample_map --genomicsdb-workspace-path outputdir/ --intervals chr01 --consolidate --batch-size 50 --reader-thread 5 --create-output-variant-index --tmp-dir=tempdir/`

3. Using GenotypeGVCFs for joint-genotyping to generate a multi-sample VCF file

    `./gatk GenotypeGVCFs --reference reference.fasta --variant gendb://path_to_genomicsdbdir --output ADM-chr01.vcf.gz --intervals chr01 -all-sites`

4. Perform hard-filtration on variant calls to remove low-quality snps and false-positives

    `./gatk VariantFiltration --reference reference.fasta \
    --variant ADM-chr01.vcf.gz \
    --intervals chr01 \
    --output ADM-chr01-filtered.vcf.gz \
    --filter-name "Low-QD" --filter-expression "QD < 0.5" \
    --filter-name "Low-FS" --filter-expression "FS > 120.0" \
    --filter-name "Low-MQ" --filter-expression "MQ < 30.0" \
    --filter-name "Low-MQRankSum" --filter-expression "MQRankSum < -8.0" \
    --filter-name "Low-ReadPosRankSum" --filter-expression "ReadPosRankSum < -8.0" \
    --filter-name "Low-SOR" --filter-expression "SOR > 8.0" \
    --filter-name "Low-AN" --filter-expression "AN < 20"`

5. Select only variants that passed the filter, and exclude indels and home-ref sites

    `./gatk SelectVariants --variant ADM-chr01-filtered.vcf.gz --output ADM-chr01-selected.vcf.gz --exclude-filtered --select-type-to-include SNP --intervals chr01`

