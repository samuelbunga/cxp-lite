filelist = getArgument();
file = split(filelist,'#');
open(file[0]);
run("Duplicate...", "duplicate range=200-3500");
run("Z Project...", "projection=[Average Intensity]");
saveAs("Tiff", file[1]);
close();
run("Quit");