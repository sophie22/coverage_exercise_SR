# Python 3.8

# Import libraries/packages for use in the code
import sys
from tracemalloc import start
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
