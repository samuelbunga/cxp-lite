import re
import sys
import csv
import openpyxl
import pandas as pd
from os import listdir
from os.path import join
from collections import defaultdict


def aggregate_features(output_dir):

    writer = pd.ExcelWriter(join(output_dir, 'aggregated_features.xlsx'))

    # Read the input directory for outputs
    output_dirs = [d for d in listdir(output_dir)
                   if d.startswith('output')]
    # Reading features csv
    # read each features file and aggregate information
    # into a dictionary
    peak_count = {}
    amplitude = {}
    auc = {}
    for f in output_dirs:
        features_csv = [j for j in listdir(join(output_dir, f))
                        if re.search(r'.*features.csv', j)][0]
        features_df = pd.read_csv(join(output_dir, f, features_csv))
        for r,c in features_df.iterrows() :
            if c[1] in peak_count:
                peak_count[c[1]].update({'cell_id': r+1, c[0]: c[2]})
                amplitude[c[1]].update({'cell_id': r+1, c[0]: c[3]})
                auc[c[1]].update({'cell_id': r+1, c[0]: c[4]})
            else:
                peak_count[c[1]] = {'cell_id': r+1, c[0]: c[2]}
                amplitude[c[1]] = {'cell_id': r+1, c[0]: c[3]}
                auc[c[1]] = {'cell_id': r+1, c[0]: c[4]}
                
                
    
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


output_dir = '../test_files/output_features/'
#aggregate_features(output_dir)
#def aggregate_wells(output_dir):

fname = '../test_files/output_features/aggregated_features.xlsx'
writer = pd.ExcelWriter('../test_files/output_features/features_average.xlsx')
wb = openpyxl.load_workbook(filename=fname, data_only=True)

# Extract sheets
peaks = wb['Peaks']
amplitude = wb['Amplitude']
auc = wb['Auc']


# Convert to pandas
columns = next(peaks.values)[0:]
peaks = pd.DataFrame(peaks.values, columns=columns)
# Drop the first row and column
peaks = peaks.drop(0)
peaks = peaks.drop(columns='cell_id')

# temporary column fix
cnames = [re.search("(.*_Timelapse_)([A-Z]\d+)", c).group(2) for c in peaks.columns.values]
peaks.columns = cnames


# get the last well number
well_id = sorted(set(re.search(r"\d+", i).group() for i in peaks.columns.values))
well_name = sorted(set([re.search(r"[A-Za-z]+", n).group() for n in peaks.columns.values]))

# create an empty dataframe
col_names = [str(i) for i in well_id]
row_names = well_name

# Create a empty dataframe
df = pd.DataFrame(columns=col_names, index=row_names, dtype=float)
df = df.fillna(0)

for c in peaks.columns.values:
    df[c[1:]][c[0]] = peaks[c].mean()

df.to_excel(writer, sheet_name ='Peaks', header=True, index=True)
writer.save()