# Identify genes with sub-optimal coverage

## Background
### Issue
The lab offers a diagnostic test for patients with either a congenital myopathy or congenital muscular dystrophy. The test sequences 83 genes that are associated with these conditions. The labwork for the test involves use of a capture kit (Agilent SureSelect) to pulldown the DNA corresponding to these genes for each patient sample. The captured DNA is then sequenced by NGS using an Illumina NextSeq. The sequence data is run through an analytical pipeline that detects variants and reports the level to which each gene has been sequenced. Performance metrics for this test require that every coding base of each gene is covered by at least 30 reads (each gene should be covered to 30x). The coverage data generation part of the pipeline is incomplete and requires some further work to produce a report that highlights any genes that are not covered at 30x.

### Current state
A tool called "sambamba" generates coverage data for each sample that has been tested. The output from sambamba lists each exon of each gene and the percentage coverage at 30x. 
- see an example output: NGS148_34_139558_CB_CMCMD_S33_R1_001.sambamba_output.txt
- the `percentage30` column in the sambamba output indicates the percentage of each region covered at >= 30x

### Task
Generate a report that lists any genes that have less than 100% coverage at 30x. Note that the sambamba output lists coverage by exon and these will need to be amalgamated to generate a list of genes that do not meet the coverage requirement.

- Ideally using python, write a script that takes the sambamba output and generates a report listing any genes that have less than 100% coverage at 30x
- This script should be able to be applied to any gene panel


# Version 0.0.1
## What is required to run this script?
A new virtual environment was created using Python 3.8.0 and packages installed from the `requirements.txt`.
The sambamba output file was converted to a tsv by replacing whitespaces with tabs by the following command: 

`sed -e 's/ /\t/g' NGS148_34_139558_CB_CMCMD_S33_R1_001.sambamba_output.txt > NGS148_34_139558_CB_CMCMD_S33_R1_001.sambamba_output.tsv`

## What does this script do?
Using the `percentage30` column, regions with less than 100% coverage at 30x are identified and a list of unique gene symbols is saved to an output file.

Command used to generate the example output: `python genes_coverage.py NGS148_34_139558_CB_CMCMD_S33_R1_001.sambamba_output.tsv`
