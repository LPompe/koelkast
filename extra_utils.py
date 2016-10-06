import os, time
import json


last_mail_time = time.time()


def get_logger(loc = '/data/logs/cameralog'):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    fh = logging.FileHandler(loc)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.info('log started')
    logger.info('starting imports ')
    return logger

def get_secrets(loc = 'secrets.json'):
    f = open('secrets.json', 'r')
    j = json.loads(f.read())
    f.close()
    return j


def send_mail(message,  target_mail, subject = 'RBPI message',):
    return os.system('echo "{}" | mail -s "{}" {}'.format(message,subject,target_mail))

def folder_size(folder = '/data/numpy_arrays'):
    folder_size = 0
    for (path, dirs, files) in os.walk(folder):
        for file in files:
            filename = os.path.join(path, file)
            folder_size += os.path.getsize(filename)
    return folder_size/(1024*1024.0)


def check_data_limit(adress, folder = '/data/numpy_arrays', limit = 15000,  ):
    #check if we are getting close to our data limit (16G)

    space = folder_size(folder = folder)
    logger.info('Checking file sizes')
    if limit - space < 1500 and time.time() - last_mail_time < MIN_MAIL_INTERVAL:
        logger.info('sending email')

        message = 'RBPI storage ({}mb) nearing maximum ({}mb). Please clear'.format(space, DATA_LIMIT)
        mail_sent = extra_utils.send_mail(message, adress) == 0
        if mail_sent:
            last_mail_time = time.time()
        else:
            logger.error('Email could not be sent')
