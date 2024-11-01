import os
import h5py
import argparse
from IPython.display import display
from IPython.core.display import HTML


# to activate python310
# > source /opt/anaconda/etc/profile.d/conda.sh
# > conda activate base
# > conda activate /SNS/users/j35/miniconda3/envs/python310

IPTS = "IPTS-33699"
NEXUS_PATH = f"/SNS/VENUS/{IPTS}/nexus/"
AUTOREDUCE_PATH = f"/SNS/VENUS/{IPTS}/shared/autoreduce/mcp/"


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


def get_collimator_value(nexus):
    with h5py.File(nexus, 'r') as hdf5_data:
        collimator = hdf5_data['entry']['DASlogs']['BL10:Mot:coll:BeamSize_RBV']['value_strings'][0][0].decode("utf8")
        return collimator


def get_slits_width(nexus):
  with h5py.File(nexus, 'r') as hdf5_data:
    slits_width = hdf5_data['entry']['DASlogs']['BL10:Mot:s1:X:Gap.RBV']['value'][:][0]
    return slits_width


def get_slits_height(nexus):
  with h5py.File(nexus, 'r') as hdf5_data:
    slits_height = hdf5_data['entry']['DASlogs']['BL10:Mot:s1:Y:Gap.RBV']['value'][:][0]
    return slits_height


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="display the PV values of the given run numbers",
                                     epilog="Example: python list_nexus_pvs.py 1534,1535,1536, 1540-1545")
    parser.add_argument('list_of_runs', type=str, nargs=1, help="List of runs (comma separated)")
    
    args = parser.parse_args()

    list_of_runs = args.list_of_runs[0]
    list_of_runs = parse_range(list_of_runs)
 
    # retrieve folder using NeXus file configtpxfilepath pv
    list_of_autoreduce_path = []
    list_frame_number = []
    list_proton_charge = []

    print(f"Run number | collimator | slits_width | slits_height")

    for _run in list_of_runs:
        nexus_path = os.path.join(NEXUS_PATH, f"VENUS_{_run}.nxs.h5")
        folder = get_file_path(nexus_path)

        collimator = get_collimator_value(nexus_path)
        slits_width = get_slits_width(nexus_path)
        slits_height = get_slits_height(nexus_path)

        print(f"{_run} | {collimator} | {slits_width} | {slits_height}")
