import os

clock_divider_file = os.path.join(os.path.dirname(__file__), "clock_divider.txt")
shutter_value_file_name = "ShutterValues.txt"

default_detector_distance_m = 25.00
default_detector_offset_us = 6500
default_shutter_file_output_folder = "/tmp"
default_beam_frequency_hz = 60

H_OVER_MN = (6.62607004e-34 / 1.674927471e-27) * 1e6

MINIMUM_LAMBDA_INTERVAL = 0.3  # minimum lambda required to correctly fit Bragg edge on either side