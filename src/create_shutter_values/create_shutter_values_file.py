import os
import pandas as pd
import numpy as np
import argparse

from create_shutter_values import H_OVER_MN

# ===
# this is using environment
# micromamba activate /SNS/users/j35/micromamba/envs/create_shutter_values_py313
# ===


# retrieve list of hkl lambda requested by user

# user select 30 or 60Hz

# ===============

# with 30Hz, 6 ranges, with 60Hz, only 3
# starting lambda must be at least 0.3A (MINIMUM_LAMBDA_INTERVAL) from first hkl requested

# format of output file
# starting time, ending time, clock divider value, 10.24 (image bin, for now this value is fixed)

from create_shutter_values import (clock_divider_file, default_detector_distance_m, default_detector_offset_us, 
                                   default_shutter_file_output_folder, default_beam_frequency_hz)

def format_list_lambda(list_lambda_in_angstroms=None):
    list_lambda_in_angstroms = list_lambda_in_angstroms.replace(" ", "")
    list_lambda_in_angstroms = list_lambda_in_angstroms.split(",")
    list_lambda = [float(_value) for _value in list_lambda_in_angstroms]

    return list_lambda

def convert_lambda_to_tof(list_lambda_in_angstroms, detector_distance_m, detector_offset_us):
    # time of flight in micro-seconds = lambda (Angstroms) * L (cm) / H_OVER_MN
    detector_distance_cm = detector_distance_m * 1e2

    list_tof_in_microseconds = [(detector_distance_cm * _lambda / H_OVER_MN) for _lambda in list_lambda_in_angstroms]
    list_tof_in_microseconds = [_tof + detector_offset_us for _tof in list_tof_in_microseconds]
    
    return list_tof_in_microseconds

def create_shutter_values_script(detector_distance_m=default_detector_distance_m, 
                                 detector_offset_us=default_detector_offset_us, 
                                 list_lambda_in_angstroms=None,
                                 beam_frequency_hz=default_beam_frequency_hz,
                                 output_folder="./"):
    
    if list_lambda_in_angstroms is None:
        raise ValueError("list_lambda_in_angstroms cannot be None")

    list_lambda_in_angstroms = format_list_lambda(list_lambda_in_angstroms)
    list_tof_in_microseconds = convert_lambda_to_tof(list_lambda_in_angstroms, detector_distance_m, detector_offset_us)
    
    print("========= Input Parameters ==========")
    print(f"* {detector_distance_m = }")
    print(f"* {detector_offset_us = }")
    print(f"* {beam_frequency_hz = }")
    print(f"* {list_lambda_in_angstroms = }")
    print(f"* {list_tof_in_microseconds = }")
    print(f"* {output_folder = }")
    print("=====================================")

    number_of_ranges = 3 if beam_frequency_hz == 60 else 6






def load_clock_divider():
    if not os.path.exists(clock_divider_file):
        raise FileNotFoundError(f"File {clock_divider_file} not found")
    
    pd_data = pd.read_csv(clock_divider_file, sep=",")
    divider = np.array(pd_data["Divider"])
    range = np.array(pd_data['Range (ms)'])

    return divider, range


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Create shutter values file for a given list of lambda',
                                     epilog='Example: python create_shutter_values.py 25.00 6500 3.4,4.6')
    parser.add_argument('--detector_distance_m', type=float, help='Distance detector_source in meters (default: %(default)s)', default=default_detector_distance_m)
    parser.add_argument('--detector_offset_us', type=float, help='Detector offset in micro-seconds (default: %(default)s)', default=default_detector_offset_us)
    parser.add_argument('--beam_frequency_hz', type=int, choices=[30, 60], help='Beam frequency in Hz (default: %(default)s)', default=default_beam_frequency_hz)
    parser.add_argument('--output_folder', type=str, help='Output folder for the shutter values file (default: %(default)s)', default=default_shutter_file_output_folder)
    parser.add_argument('list_lambda_in_angstroms', type=str, help='List of lambda in angstroms separated by comma (no space)')
    args = parser.parse_args()

    detector_distance_m = args.detector_distance_m
    if detector_distance_m is None:
        detector_distance_m = default_detector_distance_m

    detector_offset_us = args.detector_offset_us
    if detector_offset_us is None:
        detector_offset_us = default_detector_offset_us 

    list_lambda_in_angstroms = args.list_lambda_in_angstroms

    output_folder = args.output_folder
    if output_folder is None:
        output_folder = default_shutter_file_output_folder

    create_shutter_values_script(detector_distance_m, 
                                 detector_offset_us, 
                                 list_lambda_in_angstroms, 
                                 output_folder, 
                                 default_beam_frequency_hz)
