import glob
import os
import numpy as np
import shutil
from NeuNorm.normalization import Normalization
import matplotlib.pyplot as plt

import logging

# to activate python310
# > source /opt/anaconda/etc/profile.d/conda.sh
# > conda activate base
# > conda activate /SNS/users/j35/miniconda3/envs/python310

def get_list_tif(folder):
    list_tif = glob.glob(os.path.join(folder, '*.tif'))
    list_tif.sort()
    return list_tif


def load_data(folder):
    list_tif = get_list_tif(folder)
    o_norm = Normalization()
    o_norm.load(list_tif)
    return o_norm.data['sample']['data'], o_norm


log_file_name = "/SNS/users/j35/log/combine_first_2_then_3_then_n_tof_files.log"
logging.basicConfig(filename=log_file_name,
                    filemode='w',
                    format='[%(levelname)s] - %(asctime)s - %(message)s',
                    level=logging.INFO)
logging.info("*** Starting a new script 'combine_first_2_then_3_then_n_tof_files.py' ***")

top_folder = "/SNS/VENUS/IPTS-33699/shared/processed_data/"
input_folder = "NiPowder/NiPowder_testing_time_binning"

#frame_folder = "first_frame"
frame_folder = "second_frame"

full_output_folder = os.path.join(top_folder, input_folder, 'combined', frame_folder)

logging.info(f"{top_folder =}")
logging.info(f"{input_folder =}")
logging.info(f"{frame_folder =}")
logging.info(f"{full_output_folder =}")

# get list of runs
_full_input_folder = os.path.join(top_folder, input_folder, frame_folder)
logging.info(f"where to look for runs: {os.path.join(_full_input_folder, 'Run_*')}")
list_runs = glob.glob(os.path.join(_full_input_folder, "Run_*"))
logging.info(f"Found {len(list_runs)} runs!")

# sort runs
list_runs.sort()

# import matplotlib.pyplot as plt
# import numpy as np
# xaxis = np.array([2, 12, 3, 9])

# fig, ax = plt.subplots(nrows=2, ncols=2)

# # Mark each data value and customize the linestyle:
# ax[0][0].plot(xaxis, marker ='o', linestyle = '--')
# plt.show()

fig, axs = plt.subplots()

previous_combined_array = None

# move first run to final location and rename folder
combined_output_folder = os.path.join(full_output_folder, "combined_1_folder") 

if not os.path.exists(combined_output_folder):
    logging.info(f"{os.path.basename(combined_output_folder)} does not exists ... making it!")
else:
    logging.info(f"\t Removing and recreating the folder!")
    shutil.rmtree(combined_output_folder)

os.makedirs(combined_output_folder)

# moving all data from first data set to new location and loading the data
list_files = glob.glob(os.path.join(list_runs[0], "*.tif"))
for _file in list_files:
    shutil.copy(_file, combined_output_folder)
# list_files = glob.glob(os.path.join(list_runs[0], "*.fits"))
# for _file in list_files:
#     shutil.copy(_file, combined_output_folder)
list_files = glob.glob(os.path.join(list_runs[0], "*.txt"))
for _file in list_files:
    shutil.copy(_file, combined_output_folder)

# load first array
logging.info(f"\t\t loading first array .... {list_runs[0]}")
previous_combined_array, _ = load_data(list_runs[0])
logging.info(f"\t\t {np.shape(previous_combined_array) = }")
total_counts = np.sum(previous_combined_array)
logging.info(f"\t\t Total counts of previous_combined_array before adding new one {total_counts}")

sum_counts_over_y = np.sum(previous_combined_array, axis=1)
sum_counts_over_x = np.sum(sum_counts_over_y, axis=1)
axs.plot(sum_counts_over_x, label=os.path.basename(combined_output_folder))
axs.legend()
plt.show(block=False)
plt.draw()
plt.pause(0.1)

nbr_runs_to_combine = np.arange(1, len(list_runs))
for _index_last_run in nbr_runs_to_combine:
    logging.info(f"{_index_last_run}:")
    
    new_run_to_combine = list_runs[_index_last_run]
    logging.info(f"\t new run to combine: {new_run_to_combine}")

    previous_folder = combined_output_folder
    combined_output_folder = os.path.join(full_output_folder, f"combined_{_index_last_run+1}_folder")
    logging.info(f"\t will combine {os.path.basename(previous_folder)} and {os.path.basename(new_run_to_combine)} -> {os.path.basename(combined_output_folder)}")
    logging.info(f"\t output_folder will be: {combined_output_folder}")

    if not os.path.exists(combined_output_folder):
        logging.info(f"{os.path.basename(combined_output_folder)} does not exists ... making it!")
    else:
        logging.info(f"\t Removing and recreating the folder!")
        shutil.rmtree(combined_output_folder)

    os.makedirs(combined_output_folder)

    list_txt = glob.glob(os.path.join(new_run_to_combine, "*.txt"))
    for _txt in list_txt:
        shutil.copy(_txt, combined_output_folder)
    logging.info(f"\t copied {len(list_txt)} files to output location")

    # loading array of folder to combine
    new_array, o_norm = load_data(folder=new_run_to_combine)
    logging.info(f"\t\t {np.shape(new_array) = }")

    total_counts = np.sum(previous_combined_array)
    logging.info(f"\t\t Total counts before: {total_counts}")

    # combine images 1 by 1
    logging.info(f"\t\t combined images (added)")
    previous_combined_array = np.add(previous_combined_array, new_array)

    total_counts = np.sum(previous_combined_array)
    logging.info(f"\t\t Total counts after: {total_counts}")

    # output data
    o_norm.data['sample']['data'] = previous_combined_array
    o_norm.export(combined_output_folder, data_type='sample')
    logging.info(f"\t\t exported to {combined_output_folder}")

    sum_counts_over_y = np.sum(previous_combined_array, axis=1)
    sum_counts_over_x = np.sum(sum_counts_over_y, axis=1)
    axs.plot(sum_counts_over_x, label=os.path.basename(combined_output_folder))
    axs.legend()
    plt.draw()
    plt.show(block=False)
    plt.pause(0.1)

    o_norm = None

    logging.info(f"")
  
plt.show()
