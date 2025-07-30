"""Script to list NeXus PV values for specified runs on the VENUS beamline at SNS.

Usage:
    python list_nexus_pvs.py <run_numbers> [--ipts IPTS-XXXX]
    python list_nexus_pvs.py <run_numbers> --ipts IPTS-XXXX --create_output True

>> python list_nexus_pvs.py 9250 --ipts IPTS-35945

        collimator: 4x4 cm^2
        slits_width: 49.9992
        slits_height: 50.0001
        proton_charge: 11405946458630.0
        start_time: 2025-05-28T20:13:01.969076667-04:00
        end_time: 2025-05-29T07:36:15.621267667-04:00
        duration: 40993.65234375 second
        triggered_delay: 0.0
        lambda_requested: 7.0
        chopper1_phase: 16005.60242438631 us
        chopper4_phase: 31915.617873029052 us
        sample_table_position: x: -130.008, y: 125.11800000000001, z: 524.997
>>

"""
import os
import h5py
import argparse
import pandas as pd

IPTS = "IPTS-35945"
NEXUS_PATH = f"/SNS/VENUS/{IPTS}/nexus/"
AUTOREDUCE_PATH = f"/SNS/VENUS/{IPTS}/shared/autoreduce/mcp/"


def get_file_path(nexus):
    with h5py.File(nexus, 'r') as hdf5_data:
        file_path = hdf5_data["entry"]["DASlogs"]["BL10:Exp:IM:ImageFilePath"]['value'][0][0].decode("utf8")
        file_path, _run = file_path.split("/")
        return file_path
    

def parse_range(list_runs):
    result = set()
    for part in list_runs.split(','):
        x = part.split('-')
        result.update(range(int(x[0]), int(x[-1])+1))
    return sorted(result)


# ================================================
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


def get_proton_charge(nexus):
    with h5py.File(nexus, 'r') as hdf5_data:
        proton_charge = hdf5_data['entry']["proton_charge"][0]
        return proton_charge
    

def get_start_time(nexus):
    with h5py.File(nexus, 'r') as hdf5_data:
        start_time = hdf5_data['entry']['start_time'][0].decode("utf8")
        return start_time


def get_end_time(nexus):
    with h5py.File(nexus, 'r') as hdf5_data:
        end_time = hdf5_data['entry']['end_time'][0].decode("utf8")
        return end_time


def get_duration(nexus):
    with h5py.File(nexus, 'r') as hdf5_data:
        duration = hdf5_data['entry']['duration'][0]
        duration_units = hdf5_data['entry']['duration'].attrs['units'].decode("utf8 ")
        return f"{duration} {duration_units}"


def get_trigger_delay(nexus):
    with h5py.File(nexus, 'r') as hdf5_data:
        triggered_delay = hdf5_data['entry']['DASlogs']['BL10:Det:TH:BM1:TrigDelay']['value'][0]
        return triggered_delay


def get_lambda_requested(nexus):
    with h5py.File(nexus, 'r') as hdf5_data:
        lambda_requested = hdf5_data["entry"]["DASlogs"]["LambdaRequest"]['value'][0]
        return lambda_requested


def get_chopper_phase(nexus, chopper_number=1):
    with h5py.File(nexus, 'r') as hdf5_data:
        chopper = hdf5_data['entry']['instrument'][f'chopper{chopper_number}']['phase']['average_value'][0]
        chopper_units = hdf5_data['entry']['instrument'][f'chopper{chopper_number}']['phase']['average_value'].attrs['units'].decode("utf8 ")
        return f"{chopper} {chopper_units}"


def get_sample_table_position(nexus):
    with h5py.File(nexus, 'r') as hdf5_data:
        x = hdf5_data['entry']['DASlogs']['BL10:Mot:SampleX.RBV']['value'][0]
        y = hdf5_data['entry']['DASlogs']['BL10:Mot:SampleY.RBV']['value'][0]
        z = hdf5_data['entry']['DASlogs']['BL10:Mot:SampleZ.RBV']['value'][0]
        return f"x: {x}, y: {y}, z: {z}"


# ============================================

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        description="display the PV values of the given run numbers",
        epilog="Example: python list_nexus_pvs.py 1534,1535,1536, 1540-1545"
    )
    parser.add_argument('list_of_runs', type=str, nargs=1, help="List of runs (comma or dash separated)")

    # specify the IPTS
    parser.add_argument('--ipts', type=str, default=IPTS, help="Specify the IPTS (default: IPTS-35945)")

    # add an optional argument for the output file
    parser.add_argument('--create_output', type=bool, default=False, help="Output file to save the results (default: None)")

    args = parser.parse_args()

    list_of_runs = args.list_of_runs[0]
    list_of_runs = parse_range(list_of_runs)

    IPTS = args.ipts
    if IPTS:
        NEXUS_PATH = f"/SNS/VENUS/{IPTS}/nexus/"

    create_output = args.create_output

    # retrieve folder using NeXus file configtpxfilepath pv
    list_of_autoreduce_path = []
    list_frame_number = []
    list_proton_charge = []

    if create_output:
        data_dict = {
            "run_number": [],
            "collimator": [],
            "slits_width": [],
            "slits_height": [],
            "proton_charge": [],
            "start_time": [],
            "end_time": [],
            "duration": [],
            "triggered_delay": [],
            "lambda_requested": [],
            "chopper1_phase": [],
            "chopper4_phase": [],
            "sample_table_position": []
        }

    for _run in list_of_runs:
        nexus_path = os.path.join(NEXUS_PATH, f"VENUS_{_run}.nxs.h5")
        # folder = get_file_path(nexus_path)

        collimator = get_collimator_value(nexus_path)
        slits_width = get_slits_width(nexus_path)
        slits_height = get_slits_height(nexus_path)
        proton_charge = get_proton_charge(nexus_path)
        start_time = get_start_time(nexus_path)
        end_time = get_end_time(nexus_path)
        triggered_delay = get_trigger_delay(nexus_path)
        lambda_requested = get_lambda_requested(nexus_path)

        if create_output:
            data_dict["run_number"].append(_run)
            data_dict["collimator"].append(collimator)
            data_dict["slits_width"].append(slits_width)
            data_dict["slits_height"].append(slits_height)
            data_dict["proton_charge"].append(proton_charge)
            data_dict["start_time"].append(start_time)
            data_dict["end_time"].append(end_time)
            data_dict["duration"].append(get_duration(nexus_path))
            data_dict["triggered_delay"].append(triggered_delay)
            data_dict["lambda_requested"].append(lambda_requested)
            data_dict["chopper1_phase"].append(get_chopper_phase(nexus_path, chopper_number=1))
            data_dict["chopper4_phase"].append(get_chopper_phase(nexus_path, chopper_number=4))
            data_dict["sample_table_position"].append(get_sample_table_position(nexus_path))

        else:
            print(f"{_run}")
            print(f"\tcollimator: {collimator}")
            print(f"\tslits_width: {slits_width}")
            print(f"\tslits_height: {slits_height}")
            print(f"\tproton_charge: {proton_charge}")
            print(f"\tstart_time: {start_time}")
            print(f"\tend_time: {end_time}")
            print(f"\tduration: {get_duration(nexus_path)}")
            print(f"\ttriggered_delay: {triggered_delay}")
            print(f"\tlambda_requested: {lambda_requested}")
            print(f"\tchopper1_phase: {get_chopper_phase(nexus_path, chopper_number=1)}")
            print(f"\tchopper4_phase: {get_chopper_phase(nexus_path, chopper_number=4)}")
            print(f"\tsample_table_position: {get_sample_table_position(nexus_path)}")
            print(f"")

    if create_output:
        str_list_of_runs = '_'.join(map(str, list_of_runs))
        output_file_name = f"venus_pv_values_{IPTS}_runs_{str_list_of_runs}.csv"
        df = pd.DataFrame(data_dict)
        df.to_csv(output_file_name, index=False)
        print(f"Data saved to {output_file_name}")
