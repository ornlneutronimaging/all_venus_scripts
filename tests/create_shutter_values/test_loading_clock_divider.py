import numpy as np

from create_shutter_values import H_OVER_MN
from create_shutter_values.create_shutter_values_file import convert_lambda_to_tof
from create_shutter_values.create_shutter_values_file import load_clock_divider, create_shutter_values_script
from create_shutter_values.create_shutter_values_file import format_list_lambda


class TestLoadingClockDivider:

    def test_loading_clock_divider(self):
        divider_returned, range_returned = load_clock_divider()

        divider_expected = np.arange(0, 19)
        for _divider_returned, _divider_expected in zip(divider_returned, divider_expected):
            assert _divider_returned == _divider_expected

        range_expected = [0.118]
        for i in np.arange(1, len(divider_expected)+1):
            range_expected.append(range_expected[i-1] * 2)
        for _range_returned, _range_expected in zip(range_returned, range_expected):
            assert _range_returned == _range_expected
        
    def test_retrieving_parameters(self):
        detector_distance_m = 25.00
        detector_offset_us = 6500
        output_folder = "/tmp"
        
        # exception raised when list_lambda_in_angstroms is None
        try:
            create_shutter_values_script(detector_distance_m=detector_distance_m, 
                                         detector_offset_us=detector_offset_us, 
                                         output_folder=output_folder) 
        except ValueError as e:
            assert True
      
    def test_format_list_lambda(self):

        list_lambda_in_angstroms = "3. 4, 4 . 6"

        clean_list_lambda_expected = [3.4, 4.6]
        clean_list_lambda_returned = format_list_lambda(list_lambda_in_angstroms)

        for _clean_list_lambda_returned, _clean_list_lambda_expected in zip(clean_list_lambda_returned, clean_list_lambda_expected):
            assert _clean_list_lambda_returned == _clean_list_lambda_expected

    def test_convert_lambda_to_tof(self):
        list_lambda_in_angstroms = [3.4, 4.6]
        detector_distance_m = 25.00
        detector_offset_us = 6500

        detector_distance_cm = detector_distance_m * 1e2
        list_tof_in_microseconds = [(detector_distance_cm * _lambda / H_OVER_MN) for _lambda in list_lambda_in_angstroms]
        list_tof_in_microseconds_expected = [_tof + detector_offset_us for _tof in list_tof_in_microseconds]

        list_tof_in_microseconds_returned = convert_lambda_to_tof(list_lambda_in_angstroms, detector_distance_m, detector_offset_us)

        for _tof_returned, _tof_expected in zip(list_tof_in_microseconds_returned, list_tof_in_microseconds_expected):
            assert _tof_returned == _tof_expected

        tof_for_3_point_4_expected = 27986.16
        assert (tof_for_3_point_4_expected - list_tof_in_microseconds_returned[0]) < 1e-2
