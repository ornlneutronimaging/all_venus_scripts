import sys, os
import subprocess
import glob
import logging

# to activate ImagingReduction
# > source /opt/anaconda/etc/profile.d/conda.sh
# > conda activate base
# > conda activate ImagingReduction

file_name = os.path.basename(__file__)
log_file_name = f"/SNS/users/j35/log/{file_name}.log"
logging.basicConfig(filename=log_file_name,
                    filemode='w',
                    format='[%(levelname)s] - %(asctime)s - %(message)s',
                    level=logging.INFO)
logging.info(f"*** Starting a new script '{file_name}.py' ***")

cmd = 'mcp_detector_correction.py --skipimg '

input_folder = "/SNS/VENUS/IPTS-33699/images/mcp/OB_2_2C_0_7Angs_first_frame"
logging.info(f"{input_folder =}")
output_folder = "/SNS/VENUS/IPTS-33699/shared/autoreduce/mcp/"
logging.info(f"{output_folder =}")
assert os.path.exists(output_folder)

list_folder = glob.glob(os.path.join(input_folder, "Run_1674"))
logging.info(f"Found {len(list_folder)} folders!")

for _input_folder in list_folder:

    run_number = os.path.basename(_input_folder)
#    if run_number != "Run_1410":
#        print(f"skipping run {run_number}")
#        continue
#    else:
    logging.info(f"Working with run {run_number}!")
    
    _input_folder = os.path.join(_input_folder, 'tpx')

    full_output_folder = os.path.join(output_folder, run_number)
    if not os.path.exists(full_output_folder):
        os.makedirs(full_output_folder)

    full_cmd = f"{cmd} {_input_folder} {full_output_folder}"
    logging.info(f"\t {full_cmd =}")
    proc = subprocess.Popen(full_cmd,
                            shell=True,
                            stdin=subprocess.PIPE,
                            universal_newlines=True,
                            cwd=full_output_folder)
    proc.communicate()
    logging.info(f"\t done!")
