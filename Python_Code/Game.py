import numpy as np 
# import cv2 as cv 
import glob
from Camera import camera
from skimage import io, data, filters
import matplotlib.pyplot as plt
from Chess import chess


if __name__=='__main__':

    NUMSTARTPIECES = 32

    frames = sorted(glob.glob('Fools_Mate/*.jpg'))

    ch = chess(NUMSTARTPIECES)

    turnCounter = 0


    for frame in frames:
        #Debuggin be able to see what the algorthum is seeing
        currentState = ch.getBoardState


        gray = np.flip(io.imread(frame, as_gray=True),1)
        rgg_image = np.flip(io.imread(frame),1)

        src_corners = camera.findBoard(rgg_image, gray)

        cropped = camera.transformBoard(gray,src_corners, False)

        canny = camera.edgeDetector(cropped, False)

        corners = camera.cannyCorners(canny,64, cropped,False)

        camera.cleanupCorners(cropped, corners, False)

        #detect the pieces

        pieces = camera.identifyPieces(cropped, canny,32)

        currentPieces = len(pieces)

        currentState = ch.getCurrentState(corners, pieces)

        if (turnCounter > 0):

            diffState = ch.compareBoardStates(currentState)

            ch.convertStateToMove(diffState)

        ch.setBoardState(currentState)

        ch.stockfishMess()

        turnCounter = turnCounter + 1

        plt.show()
        