from skimage.io import imread
import numpy as np
import multiprocessing as mp 
import glob
import os

def _worker(fl):
    return (imread(fl).astype(np.float32)).swapaxes(0,1)


def retrieve_list_of_tif(folder):
    list_tif = glob.glob(os.path.join(folder, "*.tif*"))
    list_tif.sort()
    return list_tif


def load_data_using_multithreading(list_tif, combine_tof=False):
    with mp.Pool(processes=40) as pool:
        data = pool.map(_worker, list_tif)

    if combine_tof:
        return np.array(data).sum(axis=0)
    else:
        return np.array(data)