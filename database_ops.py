# coding: utf-8
from __future__ import print_function, division
import numpy as np
from io import BytesIO, StringIO
import pandas as pd
import pickle
import time, os, sys
from imagereader import imagereader
import image_interpreter
import logging
import h5py
from scipy import misc

class db_manager():

    def __init__(self, logger):
        self.logger = logger



    def write_image_db(self, image_tuple):

        image, t = image_tuple

        self.logger.info('scaling image')
        image_scaled = misc.imresize(image, 20)
        self.logger.info('writing image to file')
        h5f = h5py.File('/data/numpy_arrays/' + str(t), 'w')
        h5f.create_dataset('image', data=image_scaled)
        h5f.close()



if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    fh = logging.FileHandler('testdatabase.log')
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    ir = imagereader(logger)
    image =  ir.ex_image
    db_m = db_manager(logger)
    db_m.write_image_db((image, time.time()))
