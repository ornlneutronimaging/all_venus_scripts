import sys, os
import subprocess
import glob
import logging

# to activate ImagingReduction
# > source /opt/anaconda/etc/profile.d/conda.sh
# > conda activate base
# > conda activate ImagingReduction

# This script will go over all the folders of the IPTS and find for every single runs if they have been reduced or not (by looking at the autoreduce/mcp folder). 
# if they are not there, the reduction script will be triggered on that run

file_name, ext = os.path.splitext(os.path.basename(__file__))
log_file_name = f"/SNS/users/j35/log/{file_name}.log"
logging.basicConfig(filename=log_file_name,
                    filemode='w',
                    format='[%(levelname)s] - %(asctime)s - %(message)s',
                    level=logging.INFO)
logging.info(f"*** Starting a new script {file_name} ***")


cmd = 'mcp_detector_correction.py --skipimg '

ipts = 'IPTS-33699'
input_folder = f"/SNS/VENUS/{ipts}/images/mcp/"
output_folder = f"/SNS/VENUS/{ipts}/shared/autoreduce/mcp/"
logging.info(f"{input_folder =}")
logging.info(f"{output_folder =}")

assert os.path.exists(input_folder)


def that_run_has_already_been_reduced(run_number_full_path):
    """
    this checks if any tiff are found in the output folder (created using the input path)
    if they do, just return True and None
    if they don't, return False and the full path to that output folder
    if output folder does not exists, create it !
    """
    logging.info(f"\tChecking is that run has already been reduced:")
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


# list all the folders but reject the ones starting with "Run_" (wrong location for those files)
list_all_folders = [a for a in os.listdir(input_folder) if not a.startswith("Run_")]
logging.info(f"We found {len(list_all_folders) =} folders to check!")

nbr_new_runs_reduced = 0
list_new_runs_reduced_with_success = []
list_new_runs_reduced_with_error = []
nbr_runs_already_reduced = 0

for _folder in list_all_folders:

    logging.info(f"{_folder}:")
    
    # retrieve list of runs within that folder
    list_runs = glob.glob(os.path.join(input_folder, _folder, "Run_*"))
    logging.info(f"\tFound {len(list_runs)} runs in that folder!")

    for _run in list_runs:

        _state, _output_folder = that_run_has_already_been_reduced(_run)
        if _state:
            logging.info(f"\t\tAlready been reduced!")
            logging.info(f"")
            nbr_runs_already_reduced += 1
            continue
    
        _output_folder = os.path.join(_output_folder, os.path.basename(_run))
        logging.info(f"\t\tWe need to reduce run {_run} and export it to {_output_folder}")

        # because there is the extra tpx folder for now, we need to add this subfolder to the path
        _run = os.path.join(_run, 'tpx')

        full_cmd = f"{cmd} {_run} {_output_folder}"

        if not os.path.exists(_output_folder):
            os.makedirs(_output_folder)

        logging.info(f"{full_cmd =}")
        proc = subprocess.Popen(full_cmd,
                                shell=True,
                                stdin=subprocess.PIPE,
                                universal_newlines=True,
                                cwd=_output_folder)
        proc.communicate()
        logging.info(f"Done !")
        nbr_new_runs_reduced += 1    
        
        # check if there is any tiff in the output folder
        # if not, reduction failed (report it in the log)
        list_tif = glob.glob(os.path.join(_output_folder, "*.tif"))
        if len(list_tif) > 1:
            list_new_runs_reduced_with_success.append(os.path.basename(os.path.dirname(_run)))
        else:
            list_new_runs_reduced_with_error.append(os.path.basename(os.path.dirname(_run)))          

        logging.info(f"")

logging.info(f"Nbr runs process in that batch: {nbr_new_runs_reduced}")
logging.info(f"Nbr runs already reduced: {nbr_runs_already_reduced}")

logging.info(f"List of runs reduced with success in that batch: {list_new_runs_reduced_with_success}")
logging.info(f"List of runs not reduced in that batch: {list_new_runs_reduced_with_error}")
