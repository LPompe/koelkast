from collections import OrderedDict
from datetime import datetime
import h5py
import numpy as np
import os
import params

def ensure_data_folder_existence() -> None:
    """Check if the data folder exists, if not, create it."""
    folder_name = params.DATA_FOLDER_NAME
    if not folder_name in os.listdir('.'):
        os.mkdir(folder_name)


def store_sequence(sequence: OrderedDict) -> None:
    """Store a sequence of images in h5py"""
    ensure_data_folder_existence()
    file_name = datetime.now().strftime('%Y/%m/%d-%H:%M:%S')
    data_array_dims = (len(sequence), *params.IMAGE_RESOLUTION, 3)
    data = np.array(sequence.keys(), dtype=np.uint8)

    file_loc = '{}/{}.h5'.format(params.DATA_FOLDER_NAME, file_name)

    h5f = h5py.File(file_loc, 'w')
    h5f.create_dataset(file_name, data=data)
    h5f.close()
