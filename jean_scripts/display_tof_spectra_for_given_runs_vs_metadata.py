import glob
import os
import numpy as np
import shutil
from NeuNorm.normalization import Normalization
import matplotlib.pyplot as plt
import argparse
import h5py

import logging

# to activate python310
# > source /opt/anaconda/etc/profile.d/conda.sh
# > conda activate base
# > conda activate /SNS/users/j35/miniconda3/envs/python310

IPTS = "IPTS-33699"
NEXUS_PATH = f"/SNS/VENUS/{IPTS}/nexus/"
AUTOREDUCE_PATH = f"/SNS/VENUS/{IPTS}/shared/autoreduce/mcp/"


def get_list_tif(folder):
    list_tif = glob.glob(os.path.join(folder, '*.tif'))
    list_tif.sort()
    return list_tif


def load_data(folder):
    list_tif = get_list_tif(folder)
    o_norm = Normalization()
    o_norm.load(list_tif)
    return o_norm.data['sample']['data'], o_norm


def retrieve_metadata(nexus_full_path, pv_name):
    with h5py.File(nexus_full_path, 'r') as hdf5_data:
        value = hdf5_data['entry']['DASlogs'][pv_name]['value'][0]
        return value


file_name, ext = os.path.splitext(os.path.basename(__file__))
log_file_name = f"/SNS/users/j35/log/{file_name}.log"
logging.basicConfig(filename=log_file_name,
                    filemode='w',
                    format='[%(levelname)s] - %(asctime)s - %(message)s',
                    level=logging.INFO)
logging.info(f"*** Starting a new script {file_name} ***")


def run(list_runs, list_of_nexus_path, list_of_runs, list_pv_values):

    logging.info(f"{list_runs =}")
    logging.info(f"{list_pv_values =}")

    # sort runs
    list_runs.sort()

    fig, axs = plt.subplots(nrows=len(list_pv_values)+1, ncols=1)

    combined_array = None

    # load first array
    logging.info(f"\t\t loading first array .... {list_runs[0]}")
    combined_array, _ = load_data(list_runs[0])
    logging.info(f"\t\t {np.shape(combined_array) = }")
    total_counts = np.sum(combined_array)
    logging.info(f"\t\t Total counts of previous_combined_array before adding new one {total_counts}")

    label = f"{os.path.basename(list_runs[0])}"
    sum_counts_over_y = np.sum(combined_array, axis=1)
    sum_counts_over_x = np.sum(sum_counts_over_y, axis=1)
       
    axs[0].semilogy(sum_counts_over_x, label=f"{os.path.basename(list_runs[0])}")
    axs[0].set_xlabel("file index")
    axs[0].set_ylabel("Sum counts")
    
    dict_pv_values = {}
    for pv_value in list_pv_values:

        print(f"{list_runs[0] =}")

        _value = retrieve_metadata(list_of_nexus_path[0], pv_value)
        dict_pv_values[pv_value] = [_value]
      
        
    plt.show(block=False)
    plt.draw()
    plt.tight_layout()
    plt.pause(0.1)

    for nexus, run in zip(list_of_nexus_path[1:], list_of_autoreduce_path[1:]):

        logging.info(f"\tLoading {run}")
        label = f"{os.path.basename(run)}"

        new_array, o_norm = load_data(run)
        sum_counts_over_y = np.sum(new_array, axis=1)
        sum_counts_over_x = np.sum(sum_counts_over_y, axis=1)

        axs[0].semilogy(sum_counts_over_x, label=label)
        axs[0].legend()

        for pv_value in list_pv_values:
            _value = retrieve_metadata(nexus, pv_value)
            dict_pv_values[pv_value].append(_value)

        logging.info(f"")
        
        plt.draw()
      
    for index, pv_value in enumerate(dict_pv_values.keys()):

        axs[index+1].plot(dict_pv_values[pv_value], '*')
        axs[index+1].set_ylabel(pv_value)
        axs[index+1].set_xlabel("Run number")

        axs[index+1].set_xticks(np.arange(len(list_of_runs)), labels=list_of_runs)    
    

    o_norm = None

    plt.show()

def get_file_path(nexus):

    with h5py.File(nexus, 'r') as hdf5_data:
        file_path = hdf5_data["entry"]["DASlogs"]["BL10:Exp:IM:ConfigTpxFilePath"]['value'][0][0].decode("utf8")
        file_path, _run = file_path.split("/")
        return file_path
    

def parse_range(list_runs):
    result = set()
    for part in list_runs.split(','):
        x = part.split('-')
        result.update(range(int(x[0]), int(x[-1])+1))
    return sorted(result)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Display TOF profile of given run numbers and given metadata",
                                     epilog="Example: python display_tof_spectra_for_given_runs_vs_metadata 1534,1535,1536 BL10:Guide:Pres")
    parser.add_argument('list_of_runs', type=str, nargs=1, help="List of runs (comma separated)")
    parser.add_argument('pv_value', type=str, nargs=1, help="PV values (comma separated)")
    
    args = parser.parse_args()

    list_of_runs = args.list_of_runs[0]
    list_of_runs = parse_range(list_of_runs)
 
    pv_value = args.pv_value[0]
    list_pv_values = pv_value.split(",")

    # retrieve folder using NeXus file configtpxfilepath pv
    list_of_autoreduce_path = []
    list_of_nexus_path = []
    for _run in list_of_runs:
        nexus_path = os.path.join(NEXUS_PATH, f"VENUS_{_run}.nxs.h5")
        list_of_nexus_path.append(nexus_path)
        folder = get_file_path(nexus_path)
        autoreduce_path = os.path.join(AUTOREDUCE_PATH, folder, f"Run_{_run}")
        list_of_autoreduce_path.append(autoreduce_path)

    logging.info(f"{list_of_autoreduce_path =}")

    run(list_of_autoreduce_path, list_of_nexus_path, list_of_runs, list_pv_values)