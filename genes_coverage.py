#!/usr/bin/python3
# Python 3.8
"""This script is used to identify poorly covered genes

    Inputs:
        * sambamba output file in tsv format
        * optionally a coverage threshold value, which must have a
        corresponding column name in the format of 'percentageX' where X is the
        coverage threshold

    Output:
        * a file listing genes with less than 100% coverage
"""

# Import libraries/packages for use in the code
import sys
import subprocess
from pathlib import Path
import pandas as pd # v1.3.4


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

    # Calculate percentage coverage above threshold across all gene bases
    total_bases = df["ExonLength"].sum()
    bases_above_threshold = df["AboveThreshold"].sum()
    genePercentage = bases_above_threshold / total_bases * 100

    return([chromosome, startPos, endPos, GeneSymbol, Accession, genePercentage])



def main():
    ### Read inputs from  the command line
    # sambamba output file (txt)
    sambamba_txt = sys.argv[1]
    sambamba_filename = Path(sambamba_txt).stem
    sambamba_tsv = sambamba_filename + ".tsv"
    command = f"sed -e 's/ /\t/g' {sambamba_txt} > {sambamba_tsv}"
    process = subprocess.call(command, shell=True)

    # Parse sample and panel name from the input filename
    sample_name = sambamba_filename.split("_")[0]
    panel_name = sambamba_filename.split(".")[0].split("_")[4]

    ### Load sambamba output file contents into a DataFrame
    sambamba_df = pd.read_csv(sambamba_tsv, sep='\t')

    # coverage threshold (default to 30)
    if len(sys.argv) > 2:
        coverage_threshold = sys.argv[2]
    else:
        coverage_threshold = "30"
    coverage_column = "percentage" + coverage_threshold

    try:
        assert coverage_column in sambamba_df.columns, (
            f"File has no {coverage_column} column, exiting!"
        )
        print("Sambamba file loaded correctly")
    except AssertionError:
        print(f"File has no {coverage_column} column, exiting!")
        sys.exit(-1)

    # Calculate exon length by end-start position
    sambamba_df["ExonLength"] = sambamba_df["EndPosition"] - sambamba_df["StartPosition"]
    # Calculate number of bases above 30x coverage
    sambamba_df["AboveThreshold"] = sambamba_df[coverage_column] / 100 * sambamba_df["ExonLength"]

    # Identify unique genes
    panel_genes = sambamba_df["GeneSymbol;Accession"].unique().tolist()
    # Split 'GeneSymbol;Accession' into separate columns
    sambamba_df[["GeneSymbol", "Accession"]] = sambamba_df[
        "GeneSymbol;Accession"].str.split(';', 1, expand=True)

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
    out_filename = sambamba_filename.rstrip(".sambamba_output")
    outfile = out_filename + f"_suboptimal_genes_{coverage_threshold}x.tsv"
    with open(outfile, 'w') as fh:
        fh.write(f"In sample {sample_name}, the following genes of panel {panel_name} \
are not fully covered at {coverage_threshold}x: \n")
    below_threshold_genes.to_csv(outfile, sep="\t", index=False, mode='a')
    count = len(below_threshold_genes)
    print(f"Report file created listing {count} genes with suboptimal coverage")

if __name__ == "__main__":
    main()
