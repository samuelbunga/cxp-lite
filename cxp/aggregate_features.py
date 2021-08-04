import re
import sys
import csv
import pandas as pd
from os import listdir
from os.path import join
from collections import defaultdict

def aggregate_features(input_dir):
    # Read the input directory for outputs
    output_dirs = [d for d in listdir(input_dir) 
                   if d.startswith('output')]
    # Reading features csv
    for f in output_dirs:
        features_csv = [j for j in listdir(join(input_dir, f)) 
                        if re.search(r'.*features.csv', j)][0]
        features_df = pd.read_csv(join(input_dir, f, features_csv))
    # read each features file and aggregate information
    # into a dictionary
    peak_count = {}    
    for f in output_dirs:
        features_csv = [j for j in listdir(join(input_dir, f)) 
                        if re.search(r'.*features.csv', j)][0]
        features_df = pd.read_csv(join(input_dir, f, features_csv))
        for r,c in features_df.iterrows() :
            if c[1] in peak_count:
                peak_count[c[1]].update({c[0]:c[2]})
            else:
                peak_count[c[1]] = {c[0]:c[2]}

