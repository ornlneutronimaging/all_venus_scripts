import os
from PIL import Image

file_name = "/HFIR/CG1D/IPTS-27829/raw/ct_scans/October15_2021/20211015_B12W_Casting_CT_0040_2528.tiff"
assert os.path.exists(file_name)

try:
    _image = Image.open(file_name)
    metadata = dict(_image.tag_v2)
except OSError as e:
    print(f"Error opening file: {e}")
    metadata = {}


# for _key in metadata.keys():
#     print(f"{_key}: {metadata[_key]}")


print(f"{metadata[65039]}")