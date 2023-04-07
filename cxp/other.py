# All the functions here are temporary and need to be changed

import os
import re
import sys


def set_java_home():
    # os.system("export JAVA_HOME=`/usr/libexec/java_home` >>~/.bash_profile")
    # os.environ["JAVA_HOME"] = "`/usr/libexec/java_home`"
    pass


def check_mask_file(wd):
    img_files = [os.path.join(wd, f) for f in os.listdir(wd)
                 if (os.path.isfile(os.path.join(wd, f))
                     and re.search(r".*mask.*", f))
                 ]
    return True if len(img_files) >= 1 else False


def _get_non_mask(wd):
    img_files = [os.path.join(wd, f) for f in os.listdir(wd)
                 if (os.path.isfile(os.path.join(wd, f))
                     and re.search(r".*image_j.tiff", f))
                 ]
    img_files = [f for f in img_files
                 if 'mask' not in f]

    if len(img_files) >= 1:
        outfile = open(os.path.join(wd, 'data.csv'), 'w')
        with outfile as fh:
            for i in img_files:
                fh.write(i + '\n')
        return os.path.join(wd, 'data.csv')
    else:
        return False


def run_cell_profiler(pipe_file, input_folder):
    # BOOLEAN - True (mask file), False (No mask file)
    # result = check_mask_file(os.path.dirname(pipe_file))
    run_image_j(input_folder)  # Check and run imageJ on tiff files
    data_file = _get_non_mask(input_folder)
    # if not result:
    if os.path.exists(data_file) and data_file:
        os.system("cellprofiler -c -r -p " + pipe_file + " --file-list " \
                  + data_file)
    else:
        return False


def run_image_j(wd):

    img_files = [os.path.join(wd, f) for f in os.listdir(wd)
                 if (os.path.isfile(os.path.join(wd, f))
                     and not re.search(r".*image_j.*", f)
                     and not re.search(r".*mask.*", f)) and re.search(r".*[tif|tiff]$", f)
                 ]

    for i in img_files:
        input_file = os.path.basename(i.strip('\n'))
        input_file_fix = input_file.replace(" ", "_")
        os.rename(os.path.join(wd, input_file), os.path.join(wd, input_file_fix))
        input_file = input_file_fix
        output_file = os.path.basename(input_file.strip('\n')).split('.')[0] + '_image_j.tiff'
        #os.system("java -Xmx4096m -jar /Applications/ImageJ.app/Contents/Java/ij.jar -ijpath /Applications/ImageJ.app \
        os.system("/build/ImageJ/ImageJ \
        -macro " + os.path.join(os.path.dirname(__file__), 'batch.ijm ') + os.path.join(wd, input_file) + '#' + \
                  os.path.join(wd, output_file))
        # Move original files
        os.makedirs(os.path.join(wd, 'original_images')) if not os.path.exists(os.path.join(wd, 'original_images')) \
            else False
        os.rename(os.path.join(wd, input_file), os.path.join(wd, 'original_images', input_file))


if __name__ == '__main__':
    pass
