import glob
import os
import numpy as np
import shutil
from NeuNorm.normalization import Normalization
import matplotlib.pyplot as plt

import logging

# to run that code

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
logging.info(f"*** Starting a new script '{file_name}.py' ***")


instrument_path = "/SNS/VENUS"
ipts = "IPTS-33699"
folder_full_path = os.path.join(instrument_path, ipts, 'shared', 'processed_data', 'NiPowder', 'OB_NiPowder_testing_time_binning', 'first_frame')
#folder_full_path = os.path.join(instrument_path, ipts, 'shared', 'autoreduce', 'mcp', 'OB_2_2C_1_9Angs_first_frame')

list_ob_runs_nbr = [str(_run) for _run in np.arange(1664, 1673)]
list_ob_runs_nbr.remove('1671')
list_ob_runs = [f"Run_{nbr}" for nbr in list_ob_runs_nbr]
full_list_ob_runs = [os.path.join(folder_full_path, _run) for _run in list_ob_runs]

logging.info("Looking for all runs:")
for _run in full_list_ob_runs:
    if os.path.exists(_run):
        verdict = 'found'
    else:
        verdict = 'not found'
    logging.info(f"\t > {_run} -> {verdict}")

fig, axs = plt.subplots()

logging.info(f"Loading and displaying runs")
for _run in full_list_ob_runs:

    logging.info(f"\tworking with run {os.path.basename(_run)}")
    logging.info(f"\tfull file name: {_run}")
    
    list_of_images = glob.glob(os.path.join(_run, '*.tif'))
    list_of_images.sort()
    logging.info(f"\tfound {len(list_of_images)} images in that folder")

    o_norm = Normalization()
    o_norm.load(list_of_images)

    data = np.asarray(o_norm.data['sample']['data'])

    profile_2 = data.sum(axis=1)
    profile = profile_2.sum(axis=1)
   
    axs.plot(profile, label=os.path.basename(_run))
    axs.legend()
    plt.xlabel("File index")
    plt.ylabel("Sum counts")
    plt.show(block=False)
    plt.draw()
    plt.pause(0.5)
  
plt.show()
