import sys,os
import subprocess
import h5py
import pathlib
#import mcp_detector_correction
import json

CONDA_ENV = 'ImagingReduction'


def extract_image_directory(nexus_path):
    nexus = pathlib.Path(nexus_path)
    assert nexus.exists()

    with h5py.File(nexus_path, "r") as hdf5_data:
        run_number = hdf5_data["entry"]["entry_identifier"][:][0].decode("utf8")
        print(f"run_number: {run_number}")
        pv = hdf5_data["entry"]["DASlogs"]["BL3:Exp:Det:FileName"]
        print(f"pv['entry']['DASlogs']['BL3:Exp:Det:Filename']: {pv}")
        print(f"pv entries are: {pv['value'][-1][0]}")
        value = pv["value"][-1][0].decode("utf8")
        elements = value.split("/")

        return (
            pathlib.Path("/SNS/SNAP")
            / elements[2]
            / "images"
            / "mcp"
            / "/".join(elements[3:-1])
            / "Run_{}".format(run_number)
        )


def extract_ipts(nexus_path):
    nexus = pathlib.Path(nexus_path)
    assert nexus.exists()

    with h5py.File(nexus_path, "r") as hdf5_data:
        ipts = hdf5_data["entry"]["experiment_identifier"][0].decode("utf8")

        return ipts


def build_output_directory(output_dir, image_directory):
    parse_image_directory = str(image_directory).split("/")
    output_path = "/".join(parse_image_directory[5:])
    output_dir = os.path.join(output_dir, output_path)
    return output_dir


def create_full_path(output_dir):
    if os.path.exists(output_dir):
       return
    os.makedirs(output_dir)


def do_reduction(nexus_path, output_dir):

    image_directory = extract_image_directory(nexus_path)
    print(f"image_directory: {image_directory}")
    #ipts = extract_ipts(nexus_path)

    script_name = 'mcp_detector_correction.py --skipimg '
    input_dir = image_directory
    output_dir = build_output_directory(output_dir, image_directory)

    print(f"input_dir: {input_dir}")
    print(f"output_dir: {output_dir}")

    create_full_path(output_dir)

    cmd = "{0} {1} {2}".format(script_name, input_dir, output_dir)
    #cmd = (script_name, ' --skipimg ', input_dir, output_dir)

    print(f"cmd: {cmd}")
    proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                            universal_newlines = True,
                            cwd=output_dir)
    proc.communicate()
    create_summary_file(nexus_path, output_dir)


def create_summary_file(nexus_filename, output_dir):
    if not os.path.isfile(nexus_filename):
        return

    output_json = os.path.join(output_dir, "summary.json")

    f = h5py.File(nexus_filename, 'r')
    monitor1 = int(f['entry']['monitor1']['total_counts'][0])
    instrument_mode = f['entry']['DASlogs']['BL3:Exp:Mode']['value_strings'][0][0].decode("utf8")
    source_filename = f['entry']['DASlogs']['BL3:Exp:Det:FileName']['value'][0]
    source_filename = [_entry.decode("utf8") for _entry in source_filename]
    detector_offset_value = f['entry']['DASlogs']['BL3:Det:dsp1:Trig2:Delay']['average_value'][0]
    detector_offset_units = f['entry']['DASlogs']['BL3:Det:dsp1:Trig2:Delay']['average_value'].attrs.get("units").decode("utf8")
    detector_distance_value = f['entry']['DASlogs']['BL3:Exp:DetectorDistance']['average_value'][0]
    detector_distance_units = f['entry']['DASlogs']['BL3:Exp:DetectorDistance']['average_value'].attrs.get("units").decode("utf8")
    proton_charge = f['entry']['proton_charge'][0]

    _dict = {'monitor1': monitor1,
             'instrument_mode': instrument_mode,
             'source_filename': source_filename,
             'detector_offset': {'value': detector_offset_value,
                                 'units': detector_offset_units,
                                },
             'detector_distance': {'value': detector_distance_value,
                                   'units': detector_distance_units,
                                },
             'proton_charge': {'value': proton_charge,
                               'units': 'pc',
                              },
            }

    with open(output_json, 'w') as write_file:
        json.dump(_dict, write_file)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Autoreduction requires a filename and an output directory!")
        sys.exit()

    nexus_file_name = sys.argv[1]
    output_folder = sys.argv[2] + '/'

    if not (os.path.isfile(nexus_file_name)):
        print(f"nexus file name {nexus_file_name} does not exist!")
        sys.exit()

    else:

        do_reduction(nexus_file_name, output_folder)
