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


file_name = os.path.basename(__file__)
log_file_name = f"/SNS/users/j35/log/{file_name}.log"
logging.basicConfig(filename=log_file_name,
                    filemode='w',
                    format='[%(levelname)s] - %(asctime)s - %(message)s',
                    level=logging.INFO)
logging.info(f"*** Starting a new script '{file_name}.py' ***")


instrument_path = "/SNS/VENUS"
ipts = "IPTS-33699"
folder = 'SiC_CT_2_8Angs_min_5C'     # CHANGE ME
full_output_folder = os.path.join(instrument_path, ipts, 'shared', 'processed_data', folder, 'normalized')
logging.info(f"{full_output_folder =}")
if not os.path.exists(full_output_folder):
    os.makedirs(full_output_folder)

# SAMPLE
full_sample_folder = os.path.join(instrument_path, ipts, 'shared', 'autoreduce', 'mcp', folder)    # CHANGE ME
logging.info(f"{full_sample_folder =}")
assert os.path.exists(full_sample_folder)

# OB
full_ob_folder = os.path.join(instrument_path, ipts, 'shared' , 'processed_data', folder, f"OB_{folder}")    # CHANGE ME)
logging.info(f"{full_ob_folder =}")
assert os.path.exists(full_ob_folder)

# retrieving the list of sample runs
list_of_sample_folders = glob.glob(os.path.join(full_sample_folder, "Run_*"))
list_of_sample_folders.sort()
logging.info(f"Retrieving list of sample folders:")
logging.info(f"\tnumber of folders: {len(list_of_sample_folders)}")

name_of_ob_combined_folder = full_ob_folder
list_of_ob_images = glob.glob(os.path.join(name_of_ob_combined_folder, "*.tif"))
list_of_ob_images.sort()

logging.info(f"Loading OB ...")
o_ob = Normalization()
o_ob.load(list_of_ob_images)
ob_data_array = o_ob.data['sample']['data']
logging.info(f"Loading OB ... Done!")
o_ob = None

for _ob_array in ob_data_array:
    index_0 = (_ob_array == 0)
    _ob_array[index_0] = np.NaN
logging.info(f"\t{np.shape(ob_data_array) =}")

for index in np.arange(len(list_of_sample_folders)):
    
    folder_run = os.path.basename(list_of_sample_folders[index])
    logging.info(f"working with {index}/{len(list_of_sample_folders)-1}:")
    logging.info(f"\t {folder_run =}")
    full_output_folder_of_this_run = os.path.join(full_output_folder, folder_run)
    if os.path.exists(full_output_folder_of_this_run):
        shutil.rmtree(full_output_folder_of_this_run)
    os.makedirs(full_output_folder_of_this_run)
 
    logging.info(f"\t {full_output_folder_of_this_run =}")

    sample_folder = list_of_sample_folders[index]
    logging.info(f"\t {sample_folder =}")
    
    list_sample_file = glob.glob(os.path.join(sample_folder, "*.tif"))
    logging.info(f"\t will use {len(list_sample_file)} sample files")
  
    logging.info(f"\t loading data!")
    o_sample = Normalization()
    o_sample.load(list_sample_file)
    sample_data_array = o_sample.data['sample']['data']

    logging.info(f"\t{np.shape(sample_data_array) =}")
    
    norm_data = np.divide(sample_data_array, ob_data_array)

    o_sample.data['sample']['data'] = norm_data
    o_sample.export(folder=full_output_folder_of_this_run, data_type='sample')
