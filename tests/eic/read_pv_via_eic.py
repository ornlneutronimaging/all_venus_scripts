import os
import yaml
from EICClient import EICClient

IPTS = "35790"
PV_VALUE = "BL10:CS:RunControl:LastRunNumber"
BEAMLINE = "BL10"
timeout = 10

config_file = "/SNS/VENUS/IPTS-35790/shared/hype/configs/config.yaml"
assert os.path.exists(config_file)

with open(config_file, 'r') as stream:
    config = yaml.safe_load(stream)

eic_token = config['EIC_vals']['eic_token']

eic_client = EICClient(eic_token, ipts_number=IPTS, beamline=BEAMLINE)
pv_name = PV_VALUE

success_get, pv_value_read, response_data_get = eic_client.get_pv(pv_name, timeout)

if success_get:
    prefix = f'Successfully read PV {pv_name} with value {pv_value_read}'
else:
    prefix = f'Failed to read PV {pv_name}'

print(prefix)
