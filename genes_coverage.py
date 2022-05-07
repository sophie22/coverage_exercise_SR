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
# Calculate exon length by end-start position
sambamba_df["ExonLength"] = sambamba_df["EndPosition"] - sambamba_df["StartPosition"]
# Calculate number of bases above 30x coverage
sambamba_df["AboveThreshold"] = sambamba_df[coverage_column] / 100 * sambamba_df["ExonLength"]

# Identify unique genes
panel_genes = sambamba_df["GeneSymbol;Accession"].unique().tolist()
# Split 'GeneSymbol;Accession' into separate columns
sambamba_df[["GeneSymbol", "Accession"]] = sambamba_df[
    "GeneSymbol;Accession"].str.split(';', 1, expand=True)

def genePCTcovered(df):
    """
        Args: DataFrame with at least the following columns
            - 'ExonLength': which is the number of bases in the exon
            - 'AboveThreshold': which is the number of bases with reads
                above the threshold

        Returns: list of chromosome, startPos, endPos, GeneSymbol, Accession
            and the calculated genePercentage
    """
    chromosome = df["#chromosome"].to_list()[0]
    startPos = df["StartPosition"].to_list()[0]
    endPos = df["StartPosition"].to_list()[-1]
    GeneSymbol = df["GeneSymbol"].to_list()[0]
    Accession = df["Accession"].to_list()[0]

    # Calculate percentage coverage above threshold aacross all gene bases
    total_bases = df["ExonLength"].sum()
    bases_above_threshold = df["AboveThreshold"].sum()
    genePercentage = bases_above_threshold / total_bases * 100

    return([chromosome, startPos, endPos, GeneSymbol, Accession, genePercentage])

### Calculate combined coverage of genes
gene_coverage_dict = {}
for i, gene in enumerate(panel_genes):
    gene_df = sambamba_df.loc[(sambamba_df["GeneSymbol;Accession"] == gene)]
    gene_coverage_dict[i] = genePCTcovered(gene_df)

gene_coverage_df = pd.DataFrame.from_dict(gene_coverage_dict,
                    orient='index', columns=["chromosome", "startPos",
                    "endPos", "GeneSymbol", "Accession", "genePercentage"])
# Round percentage values to 2 dp
gene_coverage_df["genePercentage"] = gene_coverage_df["genePercentage"].round(2)

### Identify unique genes with at least one exon with suboptimal coverage
below_threshold_genes = gene_coverage_df[
    gene_coverage_df["genePercentage"] < 100.00
    ]

### Write gene symbols with suboptimal coverage to file
outfile = f"genes_w_suboptimal_coverage{coverage_threshold}x.txt"
with open(outfile, 'w') as fh:
    fh.write(f"The following genes are not fully covered at {coverage_threshold}x: \n")
below_threshold_genes.to_csv(outfile, sep="\t", index=False, mode='a')
