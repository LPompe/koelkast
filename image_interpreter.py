from __future__ import print_function, division
import numpy as np
import pandas as pd
import time
from imagereader import imagereader
import logging





def is_open(color_matrix):
    if color_matrix.mean() > 20:
        return True
    else:
        return False




if __name__ == "__main__":
    reader = imagereader(0)
    for matrix in reader.test_feed(10):
        print( is_open(matrix))
