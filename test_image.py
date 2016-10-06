import h5py
from scipy import misc
from imagereader import imagereader
import logging
from PIL import Image


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    fh = logging.FileHandler('testdatabase.log')
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    ir = imagereader(logger)
    rval , image = ir.camera.read()
    img = Image.fromarray(image, 'RGB')
    img.save('my.png')
    img.show()
