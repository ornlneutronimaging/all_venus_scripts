import glob
import os
import numpy as np
import shutil
from NeuNorm.normalization import Normalization
import matplotlib.pyplot as plt
import pandas as pd
import h5py

import logging

# to activate python310
# > source /opt/anaconda/etc/profile.d/conda.sh
# > conda activate base
# > conda activate /SNS/users/j35/miniconda3/envs/python310

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


def retrieve_time(nexus_full_path):
    with h5py.File(nexus_full_path, 'r') as hdf5_data:
        end_time = hdf5_data['entry']['end_time'][0].decode("utf8")[:-6]
        start_time = hdf5_data['entry']['start_time'][0].decode("utf8")[:-6]
    
    return start_time, end_time


top_input_folder = "/SNS/VENUS/IPTS-33699/shared/autoreduce/mcp/"
nexus_folder = "/SNS/VENUS/IPTS-33699/nexus/"
folder = "September6_2024_OB_5C_3_0Angsmin"

logging.info(f"{top_input_folder =}")
logging.info(f"{folder =}")

# get list of runs
_full_input_folder = os.path.join(top_input_folder, folder)
logging.info(f"where to look for runs: {os.path.join(_full_input_folder, 'Run_*')}")
list_runs = glob.glob(os.path.join(_full_input_folder, "Run_*"))
logging.info(f"Found {len(list_runs)} runs!")

# sort runs
list_runs.sort()

dict_runs = {}
start_time_array = []
end_time_array = []
for _run in list_runs:

    logging.info(f"working with {_run}")
    base_run = os.path.basename(_run)
    logging.info(f"\t{base_run =}")
    run_string, run_number = base_run.split("_")
    logging.info(f"\t{run_string =} and {run_number =}")

    # find corresponding nexus
    nexus = f"VENUS_{run_number}.nxs.h5"
    logging.info(f"\t{nexus =}")
    full_nexus_path = os.path.join(nexus_folder, nexus)
    logging.info(f"\t{full_nexus_path =}")
    assert os.path.exists(full_nexus_path)

    start_time, end_time = retrieve_time(full_nexus_path)
    start_time_array.append(start_time)
    end_time_array.append(end_time)
    logging.info(f"\t{start_time =}")
    logging.info(f"\t{end_time =}")

    dict_runs[run_number] = {'start_time': start_time,
                             'end_time': end_time}


start_time_dataframe = pd.DataFrame(start_time_array)
end_time_dataframe = pd.DataFrame(end_time_array)

start_time_list = pd.to_datetime(start_time_array)
end_time_list = pd.to_datetime(end_time_array)

ascii_file = "/SNS/VENUS/IPTS-33699/shared/processed_data/Helium_variation_studies_September6_2024/Helium_variation_September6_2024_v2"
assert os.path.exists(ascii_file)

o_pd = pd.read_csv(ascii_file, skiprows=25, names=['day_time', 'pressure1', 'pressure2'], sep='\t')
o_pd["datetime"] = pd.to_datetime(o_pd['day_time'])
logging.info(o_pd)

logging.info(f"Start: {o_pd['datetime'].min()}")
logging.info(f"End: {o_pd['datetime'].max()}")

x_axis = o_pd['datetime']
y_axis_1 = o_pd['pressure1']
y_axis_2 = o_pd['pressure2']

fig, axs = plt.subplots()
axs.plot(x_axis, y_axis_1, label='Pressure 1')
axs.plot(x_axis, y_axis_2, label='Pressure 2')
ax2 = axs.twinx()
axs.legend()
plt.xlabel("Time")

start_run = os.path.basename(list_runs[0])
end_run = os.path.basename(list_runs[-1])

axs.set_title(f"from run {start_run} to run {end_run}")
axs.set_ylabel("Pressure")
plt.draw()
plt.pause(0.1)

for _start_time, _end_time in zip(start_time_list, end_time_list):
    
    axs.axvspan(_start_time, _end_time, alpha=0.2, color='green')

for index, run in enumerate(list_runs):

    logging.info(f"\tLoading {run}")
    label = f"{os.path.basename(run)}"

    new_array, o_norm = load_data(run)
    sum_counts_over_y = np.sum(new_array, axis=1)
    sum_counts_over_x = np.sum(sum_counts_over_y, axis=1)
    median_value = np.mean(sum_counts_over_x)

    x_value = start_time_list[index]
    y_value = median_value

    ax2.plot(x_value, y_value, 'r-o')
    ax2.set_ylabel('Mean of counts')
    fig.tight_layout()
    plt.draw()
    plt.show(block=False)
    plt.pause(0.1)
  
plt.show()
