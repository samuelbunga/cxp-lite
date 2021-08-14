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
                                   'img', 'cellxpedite_logo.png')))





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