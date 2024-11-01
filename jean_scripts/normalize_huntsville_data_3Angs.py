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
logging.info(f"*** Starting a new script '{file_name}.py' ***")


instrument_path = "/SNS/VENUS"
ipts = "IPTS-33699"
top_folder = "UA_Huntsville"
folder = "NMC_3_Angs_min_UA_Huntsville"
full_output_folder = os.path.join(instrument_path, ipts, 'shared', 'processed_data', top_folder, 'normalized', folder)
logging.info(f"{full_output_folder =}")
assert os.path.exists(full_output_folder)


# SAMPLE
full_sample_folder = os.path.join(instrument_path, ipts, 'shared/processed_data', top_folder, folder) 
logging.info(f"{full_sample_folder =}")
assert os.path.exists(full_sample_folder)

# OB
full_ob_folder = os.path.join(instrument_path, ipts, 'shared/processed_data', top_folder, f"OB_{folder}")
logging.info(f"{full_ob_folder =}")
assert os.path.exists(full_ob_folder)

# retrieving list of images from sample
list_of_images = glob.glob(os.path.join(full_sample_folder, "*.tif"))
list_of_images.sort()
logging.info(f"\twill load {len(list_of_images)} sample images")

o_norm = Normalization()
o_norm.load(list_of_images)

# retrieving list of images from ob
list_of_ob_images = glob.glob(os.path.join(full_ob_folder, "*.tif"))
list_of_ob_images.sort()
logging.info(f"\twill load {len(list_of_ob_images)} ob images")

o_norm.load(list_of_ob_images, data_type='ob')                           

# normalized data
#o_norm.normalization()

sample_data = np.asarray(o_norm.data['sample']['data'])
inte_sample_1 = np.sum(sample_data, axis=1)
profile_raw = np.sum(inte_sample_1, axis=1)

ob_data = np.asarray(o_norm.data['ob']['data'])
inte_ob_1 = np.sum(ob_data, axis=1)
profile_ob = np.sum(inte_ob_1, axis=1)

#normalized_data = np.asarray(o_norm.get_normalized_data())

# normalized_data = np.divide(sample_data, ob_data)
# integration1 = normalized_data.sum(axis=1)
profile = np.divide(profile_raw, profile_ob) 

fig, axs = plt.subplots()

axs.plot(profile, label='normalized')
# axs.plot(profile_raw, label='raw')
# axs.plot(profile_ob, label='ob')
axs.legend()
plt.title(folder)
plt.xlabel("file index")
plt.ylabel("Counts")
plt.show()
