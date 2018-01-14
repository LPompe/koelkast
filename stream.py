"""All functions related to the output stream of the camera"""
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
from camera import Camera
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2, sys, os
from datetime import datetime
import numpy as np
import params
from collections import OrderedDict



def is_open(image: np.array, threshhold: float  = params.OPEN_VALUE_THRESHOLD) -> bool:
    """ determine wether the image is open, returns true if the mean value
    of the image is higher than the threshhold """

    if image.mean() > threshhold:
        return True
    else:
        return False


def get_latest_open_sequence(vs: PiVideoStream) -> OrderedDict:
    """Returns an OrderedDict of images captured during an opening of the fridge"""

    sequence = OrderedDict()
    is_currently_open = False
    prev_frame = None
    while True:
        #read one frame
        frame = vs.read()
        # if we read a valid frame, and the fridge is open, add it to the sequence
        if not frame is None and is_open(frame):

            is_currently_open = True
            frame = imutils.resize(frame, *params.IMAGE_RESOLUTION)
            # only append if we read a new frame
            sequence[frame] = None

            prev_frame = frame

        # if we read a valid frame, the fridge was open, but not anymore:
        # yield the sequence
        elif not frame is None and is_currently_open and not is_open(frame):
            return sequence
