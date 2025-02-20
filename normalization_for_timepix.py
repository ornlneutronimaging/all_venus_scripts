import argparse
import logging
import os
import h5py
import glob

LOG_PATH = "/SNS/VENUS/shared/log/"

file_name, ext = os.path.splitext(os.path.basename(__file__))
log_file_name = os.path.join(LOG_PATH, f"{file_name}.log")
logging.basicConfig(filename=log_file_name,
                    filemode='w',
                    format='[%(levelname)s] - %(asctime)s - %(message)s',
                    level=logging.INFO)
logging.info(f"*** Starting a new script {file_name} ***")






def normalization():
    pass


def retrieve_root_nexus_full_path(sample_folder):
    clean_path = os.path.abspath(sample_folder)
    if clean_path[0] == "/":
        clean_path = clean_path[1:]

    path_splitted = clean_path.split("/")
    facility = path_splitted[0]
    instrument = path_splitted[1]
    ipts = path_splitted[2]

    return f"/{facility}/{instrument}/{ipts}/nexus/"

def get_frame_number(list_nexus_path):
    dict_frame_number = {}
    for _nexus in list_nexus_path:
        try:
            with h5py.File(_nexus, 'r') as hdf5_data:
                frame_number = hdf5_data['entry']['DASlogs']['BL10:Det:PIXELMAN:ACQ:NUM']['value'][:][-1]
        except KeyError:
            frame_number = None
        dict_frame_number[os.path.basename(_nexus)] = frame_number
    return dict_frame_number

def get_proton_charge(list_nexus_path):
    dict_proton_charge = {}
    for _nexus in list_nexus_path:
        try:
            with h5py.File(_nexus, 'r') as hdf5_data:
                proton_charge = hdf5_data['entry']["proton_charge"][0] / 1e12
        except KeyError:
            proton_charge = None
        dict_proton_charge[os.path.basename(_nexus)] = proton_charge
    return dict_proton_charge

def get_list_run_number(data_folder):
    list_runs = glob.glob(os.path.join(data_folder, "Run_*"))
    list_run_number = [int(os.path.basename(run).split("_")[1]) for run in list_runs]
    return list_run_number

def get_list_nexus_full_path(nexus_root_path, list_run_numbers):
    return [os.path.join(nexus_root_path, f"VENUS_{run_number}.nxs.h5") for run_number in list_run_numbers]



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Normalized Timepix data with frame number and proton charge",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("--sample", type=str, nargs=1, help="Path to the folder containing the sample data")
    parser.add_argument("--ob", type=str, nargs=1, help="Path to the folder containing the open beam data")
    args = parser.parse_args()
    logging.info(f"{args = }")

    sample_folder = args.sample[0]
    if not os.path.exists(sample_folder):
        logging.info(f"sample folder {sample_folder} does not exist!")
        raise FileNotFoundError(f"Folder {sample_folder} does not exist!")
    else:
        logging.info(f"sample folder {sample_folder} located!")

    nexus_root_path = retrieve_root_nexus_full_path(sample_folder)
    logging.info(f"{nexus_root_path =}")

    list_sample_run_numbers = get_list_run_number(sample_folder)
    logging.info(f"{list_sample_run_numbers = }")

    list_nexus_path = get_list_nexus_full_path(nexus_root_path, list_sample_run_numbers)
    logging.info(f"{list_nexus_path = }")

    dict_frame_number = get_frame_number(list_nexus_path)
    logging.info(f"{dict_frame_number = }")

    dict_proton_charge = get_proton_charge(list_nexus_path)
    logging.info(f"{dict_proton_charge = }")





    normalization()


    # sample = /SNS/VENUS/IPTS-34808/shared/autoreduce/mcp/November17_Sample6_UA_H_Batteries_1_5_Angs_min_30Hz_5C
    # ob = /SNS/VENUS/IPTS-34808/shared/autoreduce/mcp/November17_OB_for_UA_H_Batteries_1_5_Angs_min_30Hz_5C

    # full command to use to test code
    
    # source /opts/anaconda/etc/profile.d/conda.sh
    # conda activate ImagingReduction
    # > python normalization_for_timepix.py --sample /SNS/VENUS/IPTS-34808/shared/autoreduce/mcp/November17_Sample6_UA_H_Batteries_1_5_Angs_min_30Hz_5C --ob /SNS/VENUS/IPTS-34808/shared/autoreduce/mcp/November17_OB_for_UA_H_Batteries_1_5_Angs_min_30Hz_5C