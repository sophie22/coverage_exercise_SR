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
print(sambamba_df.columns)
print(sambamba_df.head())

### Identify exons with less than 100% coverage at 30x

### Identify unique genes with at least one exon with suboptimal coverage

### Write gene symbols with suboptimal coverage to file