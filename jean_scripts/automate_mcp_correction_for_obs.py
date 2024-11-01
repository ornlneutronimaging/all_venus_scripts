import sys, os
import subprocess
import glob

# to activate ImagingReduction
# > source /opt/anaconda/etc/profile.d/conda.sh
# > conda activate base
# > conda activate ImagingReduction

cmd = 'mcp_detector_correction.py --skipimg '

folder = 'OB_NMC_3_Angs_min_UA_Huntsville'

input_folder = f"/SNS/VENUS/IPTS-33699/images/mcp/{folder}"
output_folder = f"/SNS/VENUS/IPTS-33699/shared/autoreduce/mcp/{folder}"

list_folder = glob.glob(os.path.join(input_folder, "Run_*"))
print(f"Found {len(list_folder)} folders!")

for _input_folder in list_folder:

    run_number = os.path.basename(_input_folder)
#    if run_number != "Run_1410":
#        print(f"skipping run {run_number}")
#        continue
#    else:
    print(f"Working with run {run_number}!")
    
    _input_folder = os.path.join(_input_folder, 'tpx')

    full_output_folder = os.path.join(output_folder, run_number)
    if not os.path.exists(full_output_folder):
        os.makedirs(full_output_folder)

    full_cmd = f"{cmd} {_input_folder} {full_output_folder}"
    print(f"{full_cmd =}")
    print(f"working with {run_number} ....", end="")
    proc = subprocess.Popen(full_cmd,
                            shell=True,
                            stdin=subprocess.PIPE,
                            universal_newlines=True,
                            cwd=full_output_folder)
    proc.communicate()
    print(f" done!")

