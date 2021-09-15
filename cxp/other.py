# All the functions here are temporary and need to be changed

import os
import re
import sys


def set_java_home():
    #os.system("export JAVA_HOME=`/usr/libexec/java_home` >>~/.bash_profile")
    #os.environ["JAVA_HOME"] = "`/usr/libexec/java_home`"
    pass


def check_mask_file(wd):
    img_files = [os.path.join(wd, f) for f in os.listdir(wd)
                 if (os.path.isfile(os.path.join(wd, f))
                     and re.search(r".*mask.*", f))
                 ]
    return True if len(img_files) >= 1 else False


def run_cell_profiler(pipe_file, input_folder):
    # BOOLEAN - True (mask file), False (No mask file)
    result = check_mask_file(os.path.dirname(pipe_file))
    if not result:
        os.system("/Applications/CellProfiler-3.1.9.app/Contents/MacOS/cp -c -r -p " + pipe_file + " -i "+input_folder)
    else:
        return False

def run_image_j():



if __name__ == '__main__':
    pass
