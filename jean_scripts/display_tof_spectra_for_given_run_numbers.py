import glob
import os
import numpy as np
import shutil
from NeuNorm.normalization import Normalization
import matplotlib.pyplot as plt
import argparse
import h5py
import multiprocessing as mp
from skimage.io import imread

import logging

# to activate python310
# > source /opt/anaconda/etc/profile.d/conda.sh
# > conda activate base
# > conda activate /SNS/users/j35/miniconda3/envs/python310

IPTS = "IPTS-33699"
NEXUS_PATH = f"/SNS/VENUS/{IPTS}/nexus/"
AUTOREDUCE_PATH = f"/SNS/VENUS/{IPTS}/shared/autoreduce/mcp/"

file_name, ext = os.path.splitext(os.path.basename(__file__))
log_file_name = f"/SNS/users/j35/log/{file_name}.log"
logging.basicConfig(filename=log_file_name,
                    filemode='w',
                    format='[%(levelname)s] - %(asctime)s - %(message)s',
                    level=logging.INFO)
logging.info(f"*** Starting a new script {file_name} ***")


def get_list_tif(folder):
    list_tif = glob.glob(os.path.join(folder, '*.tif'))
    list_tif.sort()
    return list_tif


def load_data(folder):
    list_tif = get_list_tif(folder)
    o_norm = Normalization()
    o_norm.load(list_tif)
    return o_norm.data['sample']['data'], o_norm

def _worker(fl):
    return (imread(fl).astype(np.float32)).swapaxes(0,1)

def load_data_mp(folder):
    list_tif = get_list_tif(folder)
    with mp.Pool(processes=20) as pool:
        data = pool.map(_worker, list_tif)

    return np.array(data)


def run(list_of_autoreduce_path):

    # top_input_folder = "/SNS/VENUS/IPTS-33699/shared/autoreduce/mcp/"
    # folder = "September6_2024_OB_5C_3_0Angsmin"

    # logging.info(f"{top_input_folder =}")
    # logging.info(f"{folder =}")

    # # get list of runs
    # _full_input_folder = os.path.join(top_input_folder, folder)
    # logging.info(f"where to look for runs: {os.path.join(_full_input_folder, 'Run_*')}")
    # list_runs = glob.glob(os.path.join(_full_input_folder, "Run_*"))
    # logging.info(f"Found {len(list_runs)} runs!")

    # list_runs = ["September9_2024_Ni_5_0C_0_7Angsmin_SA_collimators/Run_2691",
    #             "September6_2024_Ni_5_0C_0_7Angsmin/Run_2681"]
    # list_runs = [os.path.join(top_input_folder, _run) for _run in list_runs]

    # sort runs

    # import matplotlib.pyplot as plt
    # import numpy as np
    # xaxis = np.array([2, 12, 3, 9])

    # fig, ax = plt.subplots(nrows=2, ncols=2)

    # # Mark each data value and customize the linestyle:
    # ax[0][0].plot(xaxis, marker ='o', linestyle = '--')
    # plt.show()

    fig, axs = plt.subplots(nrows=2, ncols=1)

    combined_array = None

    # load first array
    logging.info(f"\t\t loading first array .... {list_of_autoreduce_path[0]}")
    
    # combined_array, _ = load_data(list_of_autoreduce_path[0])
    combined_array = load_data_mp(list_of_autoreduce_path[0])
    logging.info(f"\t\t {np.shape(combined_array) = }")
    total_counts = np.sum(combined_array)
    logging.info(f"\t\t Total counts of previous_combined_array before adding new one {total_counts}")

    label = f"{os.path.basename(list_of_autoreduce_path[0])}"
    sum_counts_over_y = np.sum(combined_array, axis=1)
    sum_counts_over_x = np.sum(sum_counts_over_y, axis=1)
    axs[0].plot(sum_counts_over_x, label=f"{os.path.basename(list_of_autoreduce_path[0])}")
    axs[0].legend()
    axs[0].set_xlabel("file index")
    axs[0].set_ylabel("Sum counts")
   
    axs[1].semilogy(sum_counts_over_x, label=f"{os.path.basename(list_of_autoreduce_path[0])}")
    axs[1].set_xlabel("file index")
    axs[1].set_ylabel("Sum counts")
    plt.show(block=False)
    plt.draw()
    plt.tight_layout()
    plt.pause(0.1)

    for run in list_of_autoreduce_path[1:]:

        logging.info(f"\tLoading {run}")
        label = f"{os.path.basename(run)}"

       # new_array, o_norm = load_data(run)
        new_array = load_data_mp(run)
        sum_counts_over_y = np.sum(new_array, axis=1)
        sum_counts_over_x = np.sum(sum_counts_over_y, axis=1)

        axs[0].plot(sum_counts_over_x, label=label)
        axs[0].legend()
        
        axs[1].semilogy(sum_counts_over_x, label=label)
        axs[1].legend()
        
        plt.draw()
        plt.show(block=False)
        plt.pause(0.1)
        plt.tight_layout()

        logging.info(f"")
    
    plt.show()

    o_norm = None


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
    
    parser = argparse.ArgumentParser(description="Display TOF profile of given run numbers",
                                     epilog="Example: python display_tof_spectra_for_given_run_numbers 1534,1535,1536")
    parser.add_argument('list_of_runs', type=str, nargs=1, help="List of runs (comma separated)")
    
    args = parser.parse_args()

    list_of_runs = args.list_of_runs[0]
    list_of_runs = parse_range(list_of_runs)
 
    # retrieve folder using NeXus file configtpxfilepath pv
    list_of_autoreduce_path = []
    for _run in list_of_runs:
        nexus_path = os.path.join(NEXUS_PATH, f"VENUS_{_run}.nxs.h5")
        folder = get_file_path(nexus_path)
        autoreduce_path = os.path.join(AUTOREDUCE_PATH, folder, f"Run_{_run}")
        list_of_autoreduce_path.append(autoreduce_path)

    logging.info(f"{list_of_autoreduce_path =}")

    run(list_of_autoreduce_path)
