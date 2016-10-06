from __future__ import print_function, division
import cv2, time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class imagereader(object):

    def __init__(self, logger, camera_n = 0):
        self.logger = logger
        self.camera_n = camera_n
        self.camera = self.establish_connection()
        rval, self.ex_image = self.camera.read()
        self.logger.debug(self.ex_image)

    def establish_connection(self):
        while True:
            try:

                camera = cv2.VideoCapture(self.camera_n)
                assert(camera.isOpened())
                return camera
            except AssertionError:

                self.logger.warning("selecting next camera")
                self.camera_n += 1
                if self.camera_n > 5:
                    self.logger.critical('Couldn\'t find valid camera')
                    raise IOError('Couldn\'t find valid camera')

    def get_feed(self):
        cam = self.camera
        rval, frame = cam.read()
        while rval:
            rval, frame = cam.read()
            yield frame

        cam.release()
        raise self.logger.criticall('Connection to camera lost')


    def test_feed(self, test_length):

        cam = self.camera

        start = time.time()

        while time.time() - start < test_length:
            rval, frame = cam.read()
            yield frame

        cam.release()

    def test_image(self, test_length, plot_rgb = False):
        cam = self.camera
        start = time.time()

        r = []
        g = []
        b = []

        while time.time() - start < test_length:
            rval, frame = cam.read()
            cv2.imshow("preview", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            frame = np.swapaxes(frame,0,2)

            if plot_rgb:
                mean_bright_r = frame[0].mean()
                mean_bright_g = frame[1].mean()
                mean_bright_b = frame[2].mean()

                r.append(mean_bright_r)
                g.append(mean_bright_g)
                b.append(mean_bright_b)

        cam.release()
        cv2.destroyWindow("preview")

        if plot_rgb:
            r = pd.Series(r)
            g = pd.Series(g)
            b = pd.Series(b)

            plt.plot(pd.concat([r,g,b], axis = 1))
            plt.show()



if __name__ == "__main__":
    reader = imagereader(0)
    #reader.test_image(10, plot_rgb = True)
    [print(x.mean()) for x in reader.test_feed(10)]
