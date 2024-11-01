import glob
import os
import numpy as np
import shutil

# to activate python310
# > source /opt/anaconda/etc/profile.d/conda.sh
# > conda activate base
# > conda activate /SNS/users/j35/miniconda3/envs/python310

# script to move first and second frame files into their own folders

top_folder = "/SNS/VENUS/IPTS-33699/shared/autoreduce/mcp/"
input_folder = "August16_2024_Nipowder_cylinder"

full_output_folder = "/SNS/VENUS/IPTS-33699/shared/processed_data/NiPowder_testing_time_binning"

# get list of runs
_full_input_folder = os.path.join(top_folder, input_folder)
print(f"where to look for runs: {os.path.join(_full_input_folder, "Run_*")}")
list_runs = glob.glob(os.path.join(_full_input_folder, "Run_*"))
print(f"Found {len(list_runs)} runs!")

first_frame_folder = os.path.join(full_output_folder, "first_frame")
second_frame_folder = os.path.join(full_output_folder, "second_frame")

for _run in list_runs:

    _base_run = os.path.basename(_run)

    list_tiff = glob.glob(os.path.join(_run, "Run_*.tif"))
    if "second_frame" in list_tiff[0]:
        _output_folder = second_frame_folder

    else:
        _output_folder = first_frame_folder

    _output_folder = os.path.join(_output_folder, _base_run)
    shutil.copytree(_run, _output_folder)  
    print(f"copied {_run} to {_output_folder}!")
