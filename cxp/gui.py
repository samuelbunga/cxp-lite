# -*- coding: utf-8 -*-

import os
import sys
import csv
import cv2
import ttk
import tkFont
import Tkinter as tk
from Tkinter import *
from ttk import Progressbar


# helper functions
def selectInputFolder():
    selectedFolder = tkFileDialog.askdirectory(title="Select input folder", initialdir='.')
    if selectedFolder:
        global input_folder
        input_folder = selectedFolder
        input_folder_basename = os.path.basename(selectedFolder)
        inputSelectedVar.set(input_folder_basename[:65])


def selectOutputFolder():
    selectedFolder = tkFileDialog.askdirectory(title="Select output folder", initialdir='.')
    if selectedFolder:
        global output_folder
        input_folder = selectedFolder
        input_folder_basename = os.path.basename(selectedFolder)
        inputSelectedVar.set(input_folder_basename[:65])


def start():
    try:
        global input_folder

        # disable start button to prevent multiple clicks
        startButton.config(state="disabled")

        # ensure input folder is specified
        if input_folder == '' or input_folder == 'no folder selected':
            tkMessageBox.showwarning("Missing user input", "An input folder must be selected.")
            return
        progress['value'] = 10
        root.update_idletasks()
        time.sleep(1)

        # identify image files
        mask_suffix = '_mask'
        mask_file_ext = '.tiff'
        img_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder)
                     if (os.path.isfile(os.path.join(input_folder, f))
                         and f != '.DS_Store'
                         and mask_suffix not in f
                         and re.search(r".*.tif[f]?", f))
                     ]

        # ensure input folder is not empty
        if len(img_files) == 0:
            tkMessageBox.showwarning("Missing data", "The input folder is empty.")
            return

        # match (img_stack, mask); ensure all mask files exist
        data = []
        for img_file in img_files:
            img_filename, img_file_extension = os.path.splitext(img_file)
            mask_file = img_filename + mask_suffix + mask_file_ext
            if os.path.isfile(mask_file):
                data.append((img_file, mask_file))
            else:
                tkMessageBox.showwarning("Missing data", "Missing mask file: \n\n" + mask_file)
                return

        # analyze each pair of files (img stack, mask)
        errors = False
        for img_file, mask_file in data:
            try:
                # create new output directory
                output_basename = os.path.basename(os.path.splitext(img_file)[0])
                output_dir = os.path.join(input_folder, 'output_' + output_basename)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                # extract time series
                fragmentsTimeSeries, background_intensity = extract_timeseries(img_file,
                                                                               mask_file,
                                                                               output_dir,
                                                                               output_basename)

                # compute time series features
                df_features = extractFeatures(fragmentsTimeSeries, background_intensity, output_dir, output_basename)

                # save df_features
                df_features.to_csv(os.path.join(output_dir, output_basename + "_features.csv"), index=False)
            except:
                errors = True

        # aggregate features
        aggregate_features(input_folder)
        progress['value'] = 70
        root.update_idletasks()
        time.sleep(1)
        progress['value'] = 100
        root.update_idletasks()

        # re-enable start button
        # output message
        if errors:
            output_status = 'Complete'
            output_message = 'Data extraction completed, but some files could not be analyzed.'
            tkMessageBox.showwarning(output_status, output_message)
        else:
            output_status = 'Success'
            output_message = 'Data extraction completed successfully.'
            tkMessageBox.showinfo(output_status, output_message)
            progress.stop()


    except Exception as e:
        # display error to user and console
        import traceback
        print(traceback.format_exc())
        tkMessageBox.showwarning("Error", "An error occured during the analysis:\n\n" + str(e))
    finally:
        startButton.config(state="normal")


# GUI frames
# params for interface
bgColor = '#d8d8d8'
btnWidth = 12
xpadding = (10,5)

# initialize interface
root = tk.Tk()
root.title('CXP')
root.resizable(width=False, height=False)
root.geometry('550x330')  # width x height
root.config(bg=bgColor)


root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file=os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   '../img', 'cellxpedite_logo.png')))





# fonts
font_buttons = tkFont.Font(root=root, family='Arial', size=14, weight='bold')
font_labels = tkFont.Font(root=root, family='Arial', size=14, weight='bold')
font_output = tkFont.Font(root=root, family='Arial', size=14)
font_filenames = tkFont.Font(root=root, family='Arial', size=12)

# MAIN FRAME
mainFrame = Frame(root, bg=bgColor, padx=10, pady=10)



# Progress bar widget
# Set Progressbar style
s = ttk.Style()
s.theme_use('clam')
s.configure("neon.Horizontal.TProgressbar", foreground='#39FF14', background='#39FF14')
progress = Progressbar(mainFrame,
                       style= "neon.Horizontal.TProgressbar",
                       orient = HORIZONTAL,
                       length = 530,
                       maximum=100,
                       cursor='coffee_mug',
                       mode = 'determinate')
progress.grid(row=14, column=0, columnspan=10,sticky=W)


print(progress)
# input file selection
selectFileBtn = Button(mainFrame, text='Select folder', command=selectInputFolder, highlightbackground=bgColor, font=font_buttons, width=btnWidth)
selectFileBtn.grid(row=0, column=0, sticky=W)

# label for selected folder
inputSelectedVar = StringVar()
inputSelectedVar.set('no folder selected')
selectedFileLabel = Label(mainFrame, textvariable=inputSelectedVar, bg=bgColor, font=font_filenames)
selectedFileLabel.grid(row=0, column=1, columnspan=5, sticky=W, padx=xpadding)

# output file selection
selectFileBtn = Button(mainFrame, text='Output folder', command=selectInputFolder, highlightbackground=bgColor, font=font_buttons, width=btnWidth)
selectFileBtn.grid(row=1, column=0, sticky=W)



# analysis params
firstk_label = Label(mainFrame, text="Start at frame", bg=bgColor, font=font_output)
firstk_label.grid(row=3, column=0, sticky=W)
firstk_entry = Entry(mainFrame, width=btnWidth)
firstk_entry.insert(END, '50')
firstk_entry.grid(row=3, column=1, sticky=W, padx=xpadding)

# smoothing params
smoothing_span_label = Label(mainFrame, text="Signal smoothing", bg=bgColor, font=font_output)
smoothing_span_label.grid(row=4, column=0, sticky=W)
smoothing_span_entry = Entry(mainFrame, width=btnWidth)
smoothing_span_entry.insert(END, '11')
smoothing_span_entry.grid(row=4, column=1, sticky=W, padx=xpadding)

# axes' parameters
xaxis_raw_label = Label(mainFrame, text="X-axis limits (Raw)", bg=bgColor, font=font_output)
xaxis_raw_label.grid(row=5, column=0, sticky=W)
xaxis_raw_entry = Entry(mainFrame, width=btnWidth)
xaxis_raw_entry.insert(END, '')
xaxis_raw_entry.grid(row=5, column=1, sticky=W, padx=xpadding)

yaxis_raw_label = Label(mainFrame, text="Y-axis limits (Raw)", bg=bgColor, font=font_output)
yaxis_raw_label.grid(row=6, column=0, sticky=W)
yaxis_raw_entry = Entry(mainFrame, width=btnWidth)
yaxis_raw_entry.insert(END, '')
yaxis_raw_entry.grid(row=6, column=1, sticky=W, padx=xpadding)

xaxis_dff_label = Label(mainFrame, text="X-axis limits (DFF)", bg=bgColor, font=font_output)
xaxis_dff_label.grid(row=7, column=0, sticky=W)
xaxis_dff_entry = Entry(mainFrame, width=btnWidth)
xaxis_dff_entry.insert(END, '')
xaxis_dff_entry.grid(row=7, column=1, sticky=W, padx=xpadding)

yaxis_dff_label = Label(mainFrame, text="Y-axis limits (DFF)", bg=bgColor, font=font_output)
yaxis_dff_label.grid(row=8, column=0, sticky=W)
yaxis_dff_entry = Entry(mainFrame, width=btnWidth)
yaxis_dff_entry.insert(END, '')
yaxis_dff_entry.grid(row=8, column=1, sticky=W, padx=xpadding)

# baseline params
baseline_fg_color = '#de5c00'
baseline_window_label = Label(mainFrame, text="Baseline window", bg=bgColor, font=font_output, fg=baseline_fg_color)
baseline_window_label.grid(row=3, column=2, sticky=W)
baseline_window_entry = Entry(mainFrame, width=btnWidth)
baseline_window_entry.insert(END, '10')
baseline_window_entry.grid(row=3, column=3, sticky=W, padx=xpadding)

baseline_quantile_label = Label(mainFrame, text="Baseline quantile", bg=bgColor, font=font_output, fg=baseline_fg_color)
baseline_quantile_label.grid(row=4, column=2, sticky=W)
baseline_quantile_entry = Entry(mainFrame, width=btnWidth)
baseline_quantile_entry.insert(END, '0.05')
baseline_quantile_entry.grid(row=4, column=3, sticky=W, padx=xpadding)

baseline_smoothing_label = Label(mainFrame, text="Baseline smoothing", bg=bgColor, font=font_output, fg=baseline_fg_color)
baseline_smoothing_label.grid(row=5, column=2, sticky=W)
baseline_smoothing_entry = Entry(mainFrame, width=btnWidth)
baseline_smoothing_entry.insert(END, '10')
baseline_smoothing_entry.grid(row=5, column=3, sticky=W, padx=xpadding)

# analysis params
peak_fg_color = 'blue'
noise_threshold_label = Label(mainFrame, text="Peak threshold", bg=bgColor, font=font_output, fg=peak_fg_color)
noise_threshold_label.grid(row=6, column=2, sticky=W)
noise_threshold_entry = Entry(mainFrame, width=btnWidth)
noise_threshold_entry.insert(END, '0.05')
noise_threshold_entry.grid(row=6, column=3, sticky=W, padx=xpadding)

min_peak_dist_label = Label(mainFrame, text="Peak distance", bg=bgColor, font=font_output, fg=peak_fg_color)
min_peak_dist_label.grid(row=7, column=2, sticky=W)
min_peak_dist_entry = Entry(mainFrame, width=btnWidth)
min_peak_dist_entry.insert(END, '5')
min_peak_dist_entry.grid(row=7, column=3, sticky=W, padx=xpadding)

peak_window_label = Label(mainFrame, text="Peak window", bg=bgColor, font=font_output, fg=peak_fg_color)
peak_window_label.grid(row=8, column=2, sticky=W)
peak_window_entry = Entry(mainFrame, width=btnWidth)
peak_window_entry.insert(END, '10')
peak_window_entry.grid(row=8, column=3, sticky=W, padx=xpadding)

min_peak_height_label = Label(mainFrame, text="Peak height", bg=bgColor, font=font_output, fg=peak_fg_color)
min_peak_height_label.grid(row=9, column=2, sticky=W)
min_peak_height_entry = Entry(mainFrame, width=btnWidth)
min_peak_height_entry.insert(END, '0.00025')
min_peak_height_entry.grid(row=9, column=3, sticky=W, padx=xpadding)

# checkbox for saving signals from active cells
savesignal_checkbox_state = IntVar()
savesignal_checkbox = Checkbutton(mainFrame, text="Save individual traces", variable=savesignal_checkbox_state, bg=bgColor, font=font_buttons)
savesignal_checkbox.grid(row=9, column=0, columnspan=2, sticky=W)  # pady=(5,0)

# start analysis
startButton = Button(mainFrame, text='Start', command=start, highlightbackground=bgColor, font=font_buttons, width=btnWidth)
startButton.grid(row=13, column=0, pady=xpadding, sticky=W)
# exit button
exitButton = Button(mainFrame, text='Exit', command=root.quit, highlightbackground=bgColor, font=font_buttons, width=btnWidth)
exitButton.grid(row=13, column=1, pady=xpadding, sticky=E)


# pack main frame
mainFrame.pack(fill='both')



# tmp fix for buttons not displaying properly
def fix():
    a = root.winfo_geometry().split('+')[0]
    b = a.split('x')
    w = int(b[0])
    h = int(b[1])
    root.geometry('%dx%d' % (w+1,h+1))
root.update()
root.after(0, fix)