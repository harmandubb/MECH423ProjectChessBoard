import numpy as np 
# import cv2 as cv 
import glob
from Camera import camera
from skimage import io, data, filters
import matplotlib.pyplot as plt
from Chess import chess


if __name__=='__main__':
    frames = glob.glob('Test_Images/miniboardfull.jpg')


    for frame in frames:
        frame_gray = io.imread(frame, as_gray=True)
        
        src_corners = camera.findBoard(frame_gray)

        frame = io.imread(frame, as_gray=True)

        cropped = camera.transformBoard(frame,src_corners)

        canny = camera.edgeDetector(cropped)

        corners = camera.cannyCorners(canny)

        print(sorted(corners, key=lambda k: [k[1], k[0]]))

        camera.cleanupCorners(cropped, corners)

        #detect the pieces

        camera.identifyPieces(cropped, canny,9)

        ch = chess()

        print(ch.board)

        plt.show()
        