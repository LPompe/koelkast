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


def store_sequence(sequence: list) -> None:
    """Store a sequence of images in h5py"""
    ensure_data_folder_existence()
    file_name = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    file_loc = '{}/{}.h5'.format(params.DATA_FOLDER_NAME, file_name)

    print("Storing h5py")
    h5f = h5py.File(file_loc, 'w')
    h5f.create_dataset('sequence', data=sequence)
    h5f.close()
    print("H5 stored")


def remove_duplicates(sequence: list) -> list:
    print("Removing duplicates")
    unique_indices = np.unique(sequence, axis=0, return_index=True)[1]
    unique_sequence = [sequence[i] for i in sorted(unique_indices)]
    print("Done removing duplicates")
    return unique_sequence
