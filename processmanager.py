# coding: utf-8
from __future__ import print_function, division
import logging



import numpy as np
from io import StringIO
import pandas as pd
import time, os, sys
#import tflearn
from imagereader import imagereader
import image_interpreter
from database_ops import db_manager
import extra_utils

DATA_LIMIT = 15000
MIN_MAIL_INTERVAL = 21600
logger = None


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

    def start(self):
        self.active = True
        self.main()

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

    def cache_image(self, image):
        self.imagecache.append(image)






def main():
    pm = processmanager(0, True)
    pm.start()


if __name__ == "__main__":
    logger = extra_utils.get_logger()
    logger.info('imports done')
    try:
        main()
    except Exception as e:
        logger.critical('process failed ' + str(e))
        os.remove('/data/pidfile.pid')
        sys.exit(e)
