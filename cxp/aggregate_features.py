import re
import sys
import csv
import openpyxl
import pandas as pd
from os import listdir
from os.path import join
from collections import defaultdict

def aggregate_features(input_dir):
    writer = pd.ExcelWriter(join(input_dir, 'aggregated_features.xlsx'))
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
    amplitude = {}
    auc = {}
    for f in output_dirs:
        features_csv = [j for j in listdir(join(input_dir, f)) 
                        if re.search(r'.*features.csv', j)][0]
        features_df = pd.read_csv(join(input_dir, f, features_csv))
        for r,c in features_df.iterrows() :
            if c[1] in peak_count:
                peak_count[c[1]].update({'cell_id':r+1, c[0]:c[2]})
                amplitude[c[1]].update({'cell_id':r+1, c[0]:c[3]})
                auc[c[1]].update({'cell_id':r+1, c[0]:c[4]})
            else:
                peak_count[c[1]] = {'cell_id':r+1, c[0]:c[2]}
                amplitude[c[1]] = {'cell_id':r+1, c[0]:c[3]}
                auc[c[1]] = {'cell_id':r+1, c[0]:c[4]}
                
                
    
    peaks_df = pd.DataFrame(peak_count).T
    peaks_df = peaks_df[peaks_df.columns.tolist()[-1:]+peaks_df.columns.tolist()[:-1]]
    
    amplitude_df = pd.DataFrame(amplitude).T
    amplitude_df = amplitude_df[amplitude_df.columns.tolist()[-1:]+amplitude_df.columns.tolist()[:-1]]
    
    auc_df = pd.DataFrame(auc).T
    auc_df = auc_df[auc_df.columns.tolist()[-1:]+auc_df.columns.tolist()[:-1]]

    
    peaks_df.to_excel(writer, sheet_name ='Peaks', header=True, index=False)
    amplitude_df.to_excel(writer, sheet_name ='Amplitude', header=True, index=False)
    auc_df.to_excel(writer, sheet_name ='Auc', header=True, index=False)
    writer.save()

