"""
Task Description: To tidy-up all CheckM output results into one text file, assuming that having many output files with similar filenames (e.g. sample_X.txt).

Here is an example of CheckM output format:
[2010-08-10 03:47:06] INFO: Reading HMM info from file.
[2010-08-10 03:47:22] INFO: Parsing HMM hits to marker genes:
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Bin Id                  Marker lineage            # genomes   # markers   # marker sets    0     1     2    3    4    5+   Completeness   Contamination   Strain heterogeneity  
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  SAMPLE.001          k__Archaea (UID2)              287         129           100         0     25    85   31   8    0       100.00           88.20             57.96          
  SAMPLE.002          k__Archaea (UID2)              350         316           190         0    312    4    0    0    0       50.00            1.90              90.00          
  SAMPLE.003          k__Bacteria (UID203)           84          568           320         1    565    2    0    0    0       80.00            9.25              10.00          
  SAMPLE.004          k__Bacteria (UID203)           235         419           211         1    397    20   1    0    0       60.53            8.23              20.04          
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
[2010-08-10 03:47:47] INFO: { Current stage: 0:00:42.830 || Total: 0:25:34.138 }

"""

import os
import pandas as pd
import numpy as np
import re

os.chdir('/path/to/all/CheckM_outputs')
print(os.getcwd())
files = [name for name in os.listdir('./') if "sample_" in name]
print("Total", str(len(files)), "output files found.")

# Read and handle record data from each output file.
df_content = []
for file in files:
    hasHeader = False
    hypen_counter = 0
    header_ = ""
    with open(file, "r") as txt:
        for line in txt.readlines():
            if "-----------------" in line:
                hypen_counter += 1
                if hypen_counter == 3:
                    break
                continue
            if hypen_counter == 1:
                header_ = re.sub('\s\s+', ',', line.strip())
            elif hypen_counter == 2:
                if not line.isspace():
                    content_ = re.sub('\s\s+', ',', line.strip())
                    if content_[0:6] == "sample":
                        df_content.append(content_.replace("\n", ""))

# Write a summary file of this task.
with open("CheckM_outputs_summary", "w") as summary:
    print("\nTotal bins throughout all samples:", len(df_content))
    summary.write("\nTotal bins throughout all samples:" + str(len(df_content)) + "\n")
    for i in range(1, len(files) + 1):
        res = "Sample" + str(i) + ":" + str(len([sample for sample in df_content if "_".join(["sample", str(i) + "."]) in sample]))
        print(res)
        summary.write(res + "\n")

# Convert string into list, by commas; then write the final record table.
header_ = list(header_.split(","))
for pos in range(len(df_content)):
    df_content[pos] = list(df_content[pos].split(","))
dataframe_bins = pd.DataFrame(data=df_content, columns=header_)
print("Size of Dataframe:", dataframe_bins.shape)
print(dataframe_bins.info())
dataframe_bins.to_csv('summary_CheckM_outputs_tidyup.csv', index=False)
