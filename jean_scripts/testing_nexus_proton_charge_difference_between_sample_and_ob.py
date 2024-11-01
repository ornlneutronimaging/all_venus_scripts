import os
import h5py
import numpy as np

# to activate python310
# > source /opt/anaconda/etc/profile.d/conda.sh
# > conda activate base
# > conda activate /SNS/users/j35/miniconda3/envs/python310

sample_nexus = "/SNS/VENUS/IPTS-33699/nexus/VENUS_3032.nxs.h5"
ob_nexus = "/SNS/VENUS/IPTS-33699/nexus/VENUS_3029.nxs.h5"
assert os.path.exists(sample_nexus)
assert os.path.exists(ob_nexus)

with h5py.File(sample_nexus, 'r') as hdf5_data:
    sample_proton_charge_array = hdf5_data['entry']['DASlogs']['proton_charge']['value'][:]
    total_proton_charge = hdf5_data['entry']['proton_charge'][0]

sample_total_counts = np.sum(sample_proton_charge_array)
print(f"sample: {sample_total_counts}")
print(f" and proton_charge reported is: {total_proton_charge}")

with h5py.File(ob_nexus, 'r') as hdf5_data:
    ob_proton_charge_array = hdf5_data['entry']['DASlogs']['proton_charge']['value'][:]

ob_total_counts = np.sum(ob_proton_charge_array)
print(f"ob: {ob_total_counts}")

print(f"ratio is {ob_total_counts/sample_total_counts}")