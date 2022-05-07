# Python 3.8

# Import libraries/packages for use in the code
import sys
import pandas as pd # v1.3.4

### Read inputs from  the command line
# sambamba output file (tsv)
sambamba_file = sys.argv[1]
# coverage threshold (default to 30)
if len(sys.argv) > 2:
    coverage_threshold = sys.argv[2]
else:
    coverage_threshold = "30"
coverage_column = "percentage" + coverage_threshold

### Load sambamba output file contents into a DataFrame
sambamba_df = pd.read_csv(sambamba_file, sep='\t')
# Split 'GeneSymbol;Accession' into separate columns
sambamba_df[["GeneSymbol", "Accession"]] = sambamba_df[
    "GeneSymbol;Accession"].str.split(';', 1, expand=True)

### Identify exons with less than 100% coverage at 30x
below_threshold_exons_df = sambamba_df[sambamba_df[coverage_column] < 100.0]

### Identify unique genes with at least one exon with suboptimal coverage
below_threshold_genes = below_threshold_exons_df["GeneSymbol"].unique().tolist()

### Write gene symbols with suboptimal coverage to file
outfile = f"genes_suboptimal_coverage{coverage_threshold}x.txt"
with open(outfile, 'w') as fh:
    for gene in below_threshold_genes:
        fh.write(gene + "\n")
