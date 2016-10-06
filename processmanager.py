# coding: utf-8
from __future__ import print_function, division
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler('log.log')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)

logger.info('log started')
logger.info('starting imports ')


import numpy as np
from io import StringIO
import pandas as pd
import time, os, sys
#import tflearn
from imagereader import imagereader
import image_interpreter
from database_ops import db_manager
from daemonize import Daemonize
import argparse
import extra_utils

DATA_LIMIT = 15000
MIN_MAIL_INTERVAL = 21600

logger.info('imports done')


class processmanager(object):

    def __init__(self, n_camera, training_mode):
        self.imagereader = imagereader(logger, n_camera)
        self.active = False
        self.ex_image = self.imagereader.ex_image
        self.imagecache = []
        self.training_mode = training_mode
        self.db_manager = db_manager(logger)
        self.last_mail_time = time.time()
        self.space_used = 0
        self.credentials = extra_utils.get_secrets()['credentials']


        if not training_mode:
            #TODO declare neural net
            pass

        logger.info("init done")

    def main(self):
        logger.info("now starting")
        while self.active:
            done = False
            for image in self.imagereader.get_feed():
                image_time = (image,  time.time())
                if image_interpreter.is_open(image):
                    self.cache_image(image_time)
                    done = False
                else:
                    if not done:
                        done = self.process_cache()




    def process_cache(self):
        if len(self.imagecache) == 0:
            logger.info('cache empty, done')
            #if we processed all the images, reset our image cache

            return True

            pass
                #TODO discretize singleton actions
                #TODO process actions
                #TODO write result to database


        if self.training_mode:
            image_time =  self.imagecache.pop()
            self.db_manager.write_image_db(image_time)
            logger.info('{} items left to process'.format(len(self.imagecache)))
        return False


    def check_data_limit(self):
        #check if we are getting close to our data limit (16G)

        space = extra_utils.folder_size()
        logger.info('Checking file sizes')
        if space != self.space_used:
            self.space_used = space
            logger.info('size on disk changed: {}'.format(self.space_used))
        if DATA_LIMIT - self.space_used < 1500 and time.time() - self.last_mail_time < MIN_MAIL_INTERVAL:
            logger.info('sending email')
            try:
                message = 'RBPI storage ({}mb) nearing maximum ({}mb). Please clear'.format(self.space_used, DATA_LIMIT)
                extra_utils.send_mail(message, self.secrets['email'])
                self.last_mail_time = time.time()
            except Exception as e:
                logger.error('Email could not be sent')




    def cache_image(self, image):
        self.imagecache.append(image)


    def start(self):
        self.active = True
        self.main()



def go():
    pm = processmanager(0, True)
    pm.start()


if __name__ == "__main__":
    try:
        go()
    except Exception as e:
        logger.critical('process failed ' + str(e))
        sys.exit(e)
