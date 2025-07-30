import sys, os
import subprocess
import glob
import logging
import argparse
from pathlib import Path

# to activate ImagingReduction
# > source /opt/anaconda/etc/profile.d/conda.sh
# > conda activate base
# > conda activate ImagingReduction

file_name, ext = os.path.splitext(os.path.basename(__file__))
log_file_name = f"/SNS/VENUS/shared/log/{file_name}.log"
logging.basicConfig(filename=log_file_name,
                    filemode='w',
                    format='[%(levelname)s] - %(asctime)s - %(message)s',
                    level=logging.INFO)
logging.info(f"*** Starting a new script {file_name} ***")

cmd = 'mcp_detector_correction.py --skipimg '

# input_folder = f"/SNS/VENUS/IPTS-33699/images/mcp/{folder_title}"
# output_folder = f"/SNS/VENUS/IPTS-33531/shared/autoreduce/mcp/"

# list_folder = glob.glob(os.path.join(input_folder, "Run_*"))
# list_folder.sort()


def that_run_has_already_been_reduced(run_number_full_path, output_folder):
    """
    this checks if any tiff are found in the output folder (created using the input path)
    if they do, just return True and None
    if they don't, return False and the full path to that output folder
    if output folder does not exists, create it !
    """
    logging.info(f"\tChecking if that run has already been reduced:")
    run_number = os.path.basename(run_number_full_path)
    logging.info(f"\t\t{run_number =}")
    folder_name = os.path.basename(os.path.dirname(run_number_full_path))
    logging.info(f"\t\t{folder_name =}")
    output_folder_name = os.path.join(output_folder, folder_name)
    if os.path.exists(output_folder_name):
        logging.info(f"\t\t{output_folder_name} does exist already - checking now that the run is there as well!")
        output_run_full_path = os.path.join(output_folder_name, run_number)
        logging.info(f"\t\t{output_run_full_path} exists?")
        if os.path.exists(output_run_full_path):
            # check that there are many tiff files there
            list_tiff_files = glob.glob(os.path.join(output_run_full_path, "*.tif*"))
            if len(list_tiff_files) > 1:
                logging.info(f"\t\tFound many tif files in that folder, it has already been reduced with success!")
                return True, None
            else:
                logging.info(f"\t\tFolder does not contain any tif files, we need to reduce that run!")
                return False, output_folder_name
        else:
            logging.info(f"{output_run_full_path} not found!")
            return False, output_folder_name
    else:
        logging.info(f"{output_folder_name} not Found!")
        return False, output_folder_name
    

def run(ipts_folder, folder_title):

    input_folder = f"/SNS/VENUS/{ipts_folder}/images/mcp/{folder_title}"
    root_output_folder = f"/SNS/VENUS/{ipts_folder}/shared/autoreduce/mcp"
    output_folder = f"{root_output_folder}/{folder_title}"

    list_folder = glob.glob(os.path.join(input_folder, "Run_*"))
    list_folder.sort()

    nbr_runs_already_reduced = 0
    nbr_new_runs_reduced = 0

    for _input_folder in list_folder:
        
        run_number = os.path.basename(_input_folder)
        print(f"Working with run {run_number} ...", end="")
        
        _state, _ = that_run_has_already_been_reduced(_input_folder, root_output_folder)

        if _state:
            logging.info(f"\t\tAlready been reduced!")
            logging.info(f"")
            print(" already reduce!")
            nbr_runs_already_reduced += 1
            continue
   
        _input_folder = os.path.join(_input_folder, 'tpx')

        full_output_folder = os.path.join(output_folder, run_number)
        if not os.path.exists(full_output_folder):
            os.makedirs(full_output_folder)

        full_cmd = f"{cmd} {_input_folder} {full_output_folder}"
        print(f"{full_cmd =}")
        print(f"working with {run_number} ....", end="")
        logging.info(f"working with {run_number}:")
        proc = subprocess.Popen(full_cmd,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True,
                                cwd=full_output_folder)
        out, err = proc.communicate()
        if err:
            logging.info(f"FAILED!")
            print(f" FAILED! (check log file at /SNS/VENUS/shared/log/{file_name})")
            logging.info(f"{err}")
        else:
            print(f" done!")
            logging.info(f" done!")
        
        nbr_new_runs_reduced += 1   

    logging.info(f"Nbr runs process in that batch: {nbr_new_runs_reduced}")
    logging.info(f"Nbr runs already reduced: {nbr_runs_already_reduced}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Reduce all the runs from the given source folder",
                                     epilog="Example: python automate_mcp_correction <folder base name only (not full path)>\npython automate_mcp_correction /SNS/VENUS/IPTS-3333/images/mcp/all_those_folders*")
    parser.add_argument('ipts', type=str, help='IPTS (IPTS-1234)')
    parser.add_argument('folder', type=str, nargs='*', help='full path to folder containing runs to reduce (MCP TimePix detector only)')
    args = parser.parse_args()

    list_folder_name = args.folder
    ipts_folder_name = args.ipts
    for _folder_name in list_folder_name:

        short_folder_name = str(Path(_folder_name).name)
        print(f"Running reduction on folder: {short_folder_name} from {ipts_folder_name}")      
        logging.info(f"Running reduction on folder: {short_folder_name} from {ipts_folder_name}")      
        run(ipts_folder_name, short_folder_name)
