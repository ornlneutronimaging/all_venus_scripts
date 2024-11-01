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


file_name, ext = os.path.splitext(os.path.basename(__file__))
log_file_name = f"/SNS/users/j35/log/{file_name}.log"
logging.basicConfig(filename=log_file_name,
                    filemode='w',
                    format='[%(levelname)s] - %(asctime)s - %(message)s',
                    level=logging.INFO)
logging.info(f"*** Starting a new script {file_name} ***")

top_input_folder = "/SNS/VENUS/IPTS-33699/shared/autoreduce/mcp/"
folder = "September6_2024_OB_5C_3_0Angsmin"

logging.info(f"{top_input_folder =}")
logging.info(f"{folder =}")

# get list of runs
_full_input_folder = os.path.join(top_input_folder, folder)
logging.info(f"where to look for runs: {os.path.join(_full_input_folder, 'Run_*')}")
list_runs = glob.glob(os.path.join(_full_input_folder, "Run_*"))
logging.info(f"Found {len(list_runs)} runs!")

list_runs = ["September9_2024_Ni_5_0C_0_7Angsmin_SA_collimators/Run_2691",
             "September6_2024_Ni_5_0C_0_7Angsmin/Run_2681"]
list_runs = [os.path.join(top_input_folder, _run) for _run in list_runs]


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
axs.plot(sum_counts_over_x, label=f"{os.path.basename(list_runs[0])}")
axs.legend()
plt.xlabel("file index")
plt.ylabel("Sum counts")
plt.show(block=False)
plt.draw()
plt.pause(0.1)

for run in list_runs[1:]:

    logging.info(f"\tLoading {run}")
    label = f"{os.path.basename(run)}"

    new_array, o_norm = load_data(run)
    sum_counts_over_y = np.sum(new_array, axis=1)
    sum_counts_over_x = np.sum(sum_counts_over_y, axis=1)

    axs.plot(sum_counts_over_x, label=label)
    axs.legend()
    plt.draw()
    plt.show(block=False)
    plt.pause(0.1)

    logging.info(f"")
  
plt.show()

o_norm = None