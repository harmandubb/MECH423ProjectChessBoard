import numpy as np 
# import cv2 as cv 
import glob
from Camera import camera
from skimage import io, data, filters
import matplotlib.pyplot as plt
from Chess import chess


if __name__=='__main__':
    frames = glob.glob('Board_Images/board13.jpg')


    for frame in frames:
        gray = np.flip(io.imread(frame, as_gray=True),1)
        rgg_image = np.flip(io.imread(frame),1)

        src_corners = camera.findBoard(rgg_image, gray)

        # gray = io.imread(frame, as_gray=True)

        

        cropped = camera.transformBoard(gray,src_corners)

        canny = camera.edgeDetector(cropped)

        corners = camera.cannyCorners(canny,64, cropped,False)

        camera.cleanupCorners(cropped, corners)

        #detect the pieces

        pieces = camera.identifyPieces(cropped, canny,32)

        ch = chess(4*8)

        currentState = ch.getCurrentState(corners, pieces)

        print(currentState)

        plt.show()
        