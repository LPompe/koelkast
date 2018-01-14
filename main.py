from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2, sys, os
from datetime import datetime
import numpy as np
import params
import stream
import data_storage

def init() -> None:
    video = PiVideoStream(resolution=params.IMAGE_RESOLUTION).start()
    #vs.camera.exposure_mode = 'sports'
    video.camera.shutter_speed = params.SHUTTER_SPEED
    video.camera.awb_gains = params.WHITE_BALANCE
    video.camera.iso = params.ISO
    time.sleep(2.0)
    main_loop(video)

def main_loop(vs: PiVideoStream) -> None:

    while True:
        latest_sequence = stream.get_latest_open_sequence(vs)
        data_storage.store_sequence(latest_sequence)
        
        
init()
