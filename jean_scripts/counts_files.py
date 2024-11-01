import glob
import pprint
import os

path = "/SNS/VENUS/IPTS-33699/images/mcp/White_beam_CT_Hematite_Magnetite_Third_Time/"

list_runs = glob.glob(path + "/Run_*")
list_runs.sort()

recap = {}

# to activate python310
# > source /opt/anaconda/etc/profile.d/conda.sh
# > conda activate base
# > conda activate /SNS/users/j35/miniconda3/envs/python310

def make_ascii_file(metadata=[], data=[], output_file_name='', dim='2d', sep=','):
    f = open(output_file_name, 'w')
    for _meta in metadata:
        _line = _meta + "\n"
        f.write(_line)

    for _data in data:
        if dim == '2d':
            _str_data = [str(_value) for _value in _data]
            _line = sep.join(_str_data) + "\n"
        else:
            _line = str(_data) + '\n'
        f.write(_line)

    f.close()


for _run in list_runs:
	list_files = glob.glob(_run + "/tpx/*.fits")
	list_files.sort()
	first_angle = list_files[0]
	last_angle = list_files[-1]
	
	recap[os.path.basename(_run)] = {'nbr_files': len(list_files),
		       'first_angle': os.path.basename(first_angle),
		       'last_angle': os.path.basename(last_angle),
		
		       }
		 
pprint.pprint(recap)

to_export_data = []
for _key in recap.keys():
	_run = _key
	_nbr_files = recap[_key]['nbr_files']
	_first = recap[_key]['first_angle']
	_last = recap[_key]['last_angle']
	_line = f"{_run} has {_nbr_files} from angle {_first} to {_last}"
	to_export_data.append(_line)
	
output_file_name = "/SNS/users/j35/testing_file_structure_ipts_33699.csv"
make_ascii_file(data=to_export_data, output_file_name=output_file_name, dim='1d')

