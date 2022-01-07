import re
import sys
import csv
import numpy as np
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
        for r, c in features_df.iterrows():
            if c[1] in peak_count:
                peak_count[c[1]].update({'cell_id': r + 1, c[0]: c[2]})
                amplitude[c[1]].update({'cell_id': r + 1, c[0]: c[3]})
                auc[c[1]].update({'cell_id': r + 1, c[0]: c[4]})
            else:
                peak_count[c[1]] = {'cell_id': r + 1, c[0]: c[2]}
                amplitude[c[1]] = {'cell_id': r + 1, c[0]: c[3]}
                auc[c[1]] = {'cell_id': r + 1, c[0]: c[4]}

    peaks_df = pd.DataFrame(peak_count).T
    # peaks_df = peaks_df[peaks_df.columns.tolist()[-1:]+peaks_df.columns.tolist()[:-1]]

    amplitude_df = pd.DataFrame(amplitude).T
    # amplitude_df = amplitude_df[amplitude_df.columns.tolist()[-1:]+amplitude_df.columns.tolist()[:-1]]

    auc_df = pd.DataFrame(auc).T
    # auc_df = auc_df[auc_df.columns.tolist()[-1:]+auc_df.columns.tolist()[:-1]]

    peaks_df.to_excel(writer, sheet_name='Peaks', header=True, index=False)
    amplitude_df.to_excel(writer, sheet_name='Amplitude', header=True, index=False)
    auc_df.to_excel(writer, sheet_name='Auc', header=True, index=False)
    writer.save()


def _xlsx_to_df(sheets):
    Dfs = []
    for s in sheets:
        # Convert to pandas
        columns = next(s.values)[0:]
        s = pd.DataFrame(s.values, columns=columns)
        # Drop the first row and column
        s = s.drop(0)
        s = s.drop(columns='cell_id')
        s.fillna(value=np.nan, inplace=True)
        Dfs.append(s)
    return Dfs


def _calculate_avg_active_wells(Dfs, output_dir):
    peaks_df = Dfs[0]
    count = int(0)
    avg_wells = pd.ExcelWriter(join(output_dir, 'average_wells.xlsx'))
    active_wells = pd.ExcelWriter(join(output_dir, 'active_wells.xlsx'))

    well_id = sorted(set(re.search(r"\d+", i).group() for i in peaks_df.columns.values))
    well_name = sorted(set([re.search(r"[A-Za-z]+", n).group() for n in peaks_df.columns.values]))

    # create an empty dataframe
    col_names = [str(i) for i in well_id]
    row_names = well_name

    # Total neuron
    active_neuron = pd.DataFrame(columns=col_names, index=row_names, dtype=float)
    total_neuron = pd.DataFrame(columns=col_names, index=row_names, dtype=float)
    # Fill empty values with 0
    active_neuron.fillna(0)
    total_neuron.fillna(0)
    print(peaks_df)
    for c in peaks_df.columns.values:
        active_neuron[c[1:]][c[0]] = len([a for a in peaks_df[c] if a > 0])
        total_neuron[c[1:]][c[0]] = len([a for a in peaks_df[c] if a >= 0])

    # -----------------

    # Total spikes
    total_spikes = pd.DataFrame(columns=col_names, index=row_names, dtype=float)
    # Fill empty values with 0
    total_spikes.fillna(0)

    for c in peaks_df.columns.values:
        total_spikes[c[1:]][c[0]] = sum([a for a in peaks_df[c] if a >= 0])

    # active peaks
    active_peaks = pd.DataFrame(columns=col_names, index=row_names, dtype=float)
    # Fill empty values with 0
    active_peaks.fillna(0)

    for c in peaks_df.columns.values:
        peaks_counts = sum([a for a in peaks_df[c] if a > 0])
        active_neurons = len([a for a in peaks_df[c] if a > 0])
        if active_neurons == 0:
            active_peaks[c[1:]][c[0]] = 0
        else:
            active_peaks[c[1:]][c[0]] = peaks_counts / float(active_neurons)
    active_peaks.to_excel(active_wells, sheet_name='Active_peaks', header=True, index=True)

    for df in Dfs:
        # Get unique well ids
        well_id = sorted(set(re.search(r"\d+", i).group() for i in df.columns.values))
        well_name = sorted(set([re.search(r"[A-Za-z]+", n).group() for n in df.columns.values]))

        # create an empty dataframe
        col_names = [str(i) for i in well_id]
        row_names = well_name

        # Create a empty dataframe from active and average wells
        active_df = pd.DataFrame(columns=col_names, index=row_names, dtype=float)
        avg_df = pd.DataFrame(columns=col_names, index=row_names, dtype=float)
        # Fill empty values with 0
        active_df.fillna(0)
        avg_df.fillna(0)

        # Calculate average wells / active wells
        for c in df.columns.values:
            avg_df[c[1:]][c[0]] = df[c].mean()
            if sheet_names[count] == 'Amplitude' or sheet_names[count] == 'AUC':
                active_df[c[1:]][c[0]] = sum([a for a in df[c] if a > 0]) / active_neuron[c[1:]][c[0]]
            else:
                active_df[c[1:]][c[0]] = len([a for a in df[c] if a > 0])

        avg_df.to_excel(avg_wells, sheet_name=sheet_names[count], header=True, index=True)

        if sheet_names[count] != 'Peaks':
            active_df.to_excel(active_wells, sheet_name=sheet_names[count], header=True, index=True)
        count += 1

    active_neuron.to_excel(active_wells, sheet_name='Active_neuron', header=True, index=True)
    total_neuron.to_excel(avg_wells, sheet_name='Total_neuron', header=True, index=True)
    total_spikes.to_excel(active_wells, sheet_name='Total_spikes', header=True, index=True)
    total_spikes.to_excel(avg_wells, sheet_name='Total_spikes', header=True, index=True)
    avg_wells.save()
    active_wells.save()


def aggregate_wells(output_dir):
    fname = join(output_dir, 'aggregated_features.xlsx')
    wb = openpyxl.load_workbook(filename=fname, data_only=True)

    # Extract sheets
    peaks = wb['Peaks']
    amplitude = wb['Amplitude']
    auc = wb['Auc']

    # Declare global sheet names
    global sheet_names
    sheet_names = ['Peaks', 'Amplitude', 'AUC']
    sheets = [peaks, amplitude, auc]

    Dfs = _xlsx_to_df(sheets)
    _calculate_avg_active_wells(Dfs, output_dir)
